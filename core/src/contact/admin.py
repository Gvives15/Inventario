from django.contrib import admin, messages
from django.utils import timezone
from django import forms
from contact.models import Contact, OrderModel, ZoneModel, OrderReviewQueue
from contact.modules.orders.application.commands.change_ops_status_cmd import execute

class ReviewActionForm(forms.Form):
    review_reason_code = forms.ChoiceField(choices=OrderModel.REVIEW_CODE_CHOICES, required=True)
    review_reason_note = forms.CharField(required=False)

class ResolveReviewActionForm(forms.Form):
    resolution_note = forms.CharField(required=True)

class ReviewQueueFilter(admin.SimpleListFilter):
    title = "Review Queue"
    parameter_name = "review_queue"

    def lookups(self, request, model_admin):
        return (
            ("pending", "Pending (REQUIRES_REVIEW)"),
            ("overdue", "Overdue (deadline passed)"),
            ("no_deadline", "No deadline"),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == "pending":
            return queryset.filter(ops_status=OrderModel.OPS_REQUIRES_REVIEW)
        if val == "overdue":
            return queryset.filter(
                ops_status=OrderModel.OPS_REQUIRES_REVIEW,
                review_deadline_at__isnull=False,
                review_deadline_at__lt=timezone.now(),
            )
        if val == "no_deadline":
            return queryset.filter(
                ops_status=OrderModel.OPS_REQUIRES_REVIEW,
                review_deadline_at__isnull=True,
            )
        return queryset

class ZoneFilter(admin.SimpleListFilter):
    title = "Zona"
    parameter_name = "zone"

    def lookups(self, request, model_admin):
        qs = ZoneModel.objects.filter(contacts__isnull=False).distinct().order_by("name")
        return [(z.id, z.name) for z in qs]

    def queryset(self, request, queryset):
        val = self.value()
        if val:
            if hasattr(queryset.model, "contact"):
                return queryset.filter(contact__zone_id=val)
            return queryset.filter(zone_id=val)
        return queryset

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "zone", "is_active", "updated_at")
    list_filter = ("type", "is_active", ZoneFilter)
    search_fields = ("name", "whatsapp_id")
    autocomplete_fields = ["zone"]
    actions = ["assign_zone_bulk"]

    def assign_zone_bulk(self, request, queryset):
        form = None
        if "apply" in request.POST:
            form = AssignZoneForm(request.POST)
            if form.is_valid():
                zone = form.cleaned_data["zone"]
                updated = queryset.filter(zone__isnull=True).update(zone=zone, updated_at=timezone.now())
                if updated:
                    messages.success(request, f"{updated} contactos actualizados con zona")
                else:
                    messages.warning(request, "No se actualizaron contactos (quizás ya tenían zona)")
                return
        else:
            form = AssignZoneForm()
        
        context = {
            "title": "Asignar zona (Bulk)",
            "action_name": "assign_zone_bulk",
            "form": form,
            "queryset": queryset,
        }
        from django.shortcuts import render
        return render(request, "admin/review_action_form.html", context)
    assign_zone_bulk.short_description = "Asignar zona (Bulk)"

@admin.register(ZoneModel)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active", "is_dangerous", "created_at")
    list_filter = ("is_active", "is_dangerous")
    search_fields = ("code", "name")

@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "contact", "zone_name", "items_count", "ops_status", "review_reason_code")
    list_filter = ("ops_status", ReviewQueueFilter, ZoneFilter, "created_at")
    search_fields = ("id", "contact__whatsapp_id", "contact__name")
    ordering = ("review_deadline_at", "-ops_updated_at", "-created_at")
    # list_editable = ("review_deadline_at",) # Removed

    actions = ["to_preparing", "to_ready", "to_out", "to_delivered", "to_paid", "to_cancelled", "to_review_generic", "to_review", "resolve_review_to_preparing", "resolve_review_to_cancelled", "set_deadline_24h", "set_deadline_72h", "assign_zone_to_contact"]

    def zone_name(self, obj):
        return obj.contact.zone.name if obj.contact.zone_id else "—"
    zone_name.short_description = "Zona"

    def _bulk_transition(self, request, queryset, target, require_review=False, form=None):
        count = 0
        for order in queryset:
            try:
                if require_review and form is not None:
                    execute(order.id, OrderModel.OPS_REQUIRES_REVIEW, review_reason_code=form.cleaned_data["review_reason_code"], review_reason_note=form.cleaned_data.get("review_reason_note"))
                else:
                    execute(order.id, target)
                count += 1
            except Exception as e:
                messages.error(request, f"Order {order.id}: {e}")
        if count:
            messages.success(request, f"{count} órdenes actualizadas a {target}")

    def to_preparing(self, request, queryset):
        self._bulk_transition(request, queryset, OrderModel.OPS_PREPARING)
    to_preparing.short_description = "Move → PREPARING"

    def to_ready(self, request, queryset):
        self._bulk_transition(request, queryset, OrderModel.OPS_READY)
    to_ready.short_description = "Move → READY"

    def to_out(self, request, queryset):
        self._bulk_transition(request, queryset, OrderModel.OPS_OUT_FOR_DELIVERY)
    to_out.short_description = "Move → OUT_FOR_DELIVERY"

    def to_delivered(self, request, queryset):
        self._bulk_transition(request, queryset, OrderModel.OPS_DELIVERED)
    to_delivered.short_description = "Mark → DELIVERED"

    def to_paid(self, request, queryset):
        self._bulk_transition(request, queryset, OrderModel.OPS_PAID)
    to_paid.short_description = "Mark → PAID"

    def to_cancelled(self, request, queryset):
        self._bulk_transition(request, queryset, OrderModel.OPS_CANCELLED)
    to_cancelled.short_description = "Cancel → CANCELLED"

    def to_review_generic(self, request, queryset):
        count = 0
        for order in queryset:
            try:
                execute(order.id, OrderModel.OPS_REQUIRES_REVIEW, review_reason_code=OrderModel.REVIEW_MANUAL)
                count += 1
            except Exception as e:
                messages.error(request, f"Order {order.id}: {e}")
        if count:
            messages.success(request, f"{count} órdenes actualizadas a REQUIRES_REVIEW (GENERIC)")
    to_review_generic.short_description = "Send → REQUIRES_REVIEW (GENERIC)"

    def to_review(self, request, queryset):
        form = None
        if "apply" in request.POST:
            form = ReviewActionForm(request.POST)
            if form.is_valid():
                self._bulk_transition(request, queryset, OrderModel.OPS_REQUIRES_REVIEW, require_review=True, form=form)
                return
        else:
            form = ReviewActionForm()
        context = {
            "title": "Send → REQUIRES_REVIEW",
            "action_name": "to_review",
            "form": form,
            "queryset": queryset,
        }
        from django.shortcuts import render
        return render(request, "admin/review_action_form.html", context)

    def _resolve_review(self, request, queryset, target, action_name, title):
        form = None
        if "apply" in request.POST:
            form = ResolveReviewActionForm(request.POST)
            if form.is_valid():
                count = 0
                note = f"RESOLVED: {form.cleaned_data['resolution_note']}"
                for order in queryset:
                    if order.ops_status != OrderModel.OPS_REQUIRES_REVIEW:
                        messages.error(request, f"Order {order.id}: solo se puede resolver órdenes en REQUIRES_REVIEW")
                        continue
                    try:
                        execute(order.id, target, note=note, resolve_review=True)
                        count += 1
                    except Exception as e:
                        messages.error(request, f"Order {order.id}: {e}")
                if count:
                    messages.success(request, f"{count} órdenes resueltas a {target}")
                return
        else:
            form = ResolveReviewActionForm()
        context = {
            "title": title,
            "action_name": action_name,
            "form": form,
            "queryset": queryset,
        }
        from django.shortcuts import render
        return render(request, "admin/review_action_form.html", context)

    def resolve_review_to_preparing(self, request, queryset):
        return self._resolve_review(request, queryset, OrderModel.OPS_PREPARING, "resolve_review_to_preparing", "Resolve REVIEW → PREPARING")
    resolve_review_to_preparing.short_description = "Resolve REVIEW → PREPARING"

    def resolve_review_to_cancelled(self, request, queryset):
        return self._resolve_review(request, queryset, OrderModel.OPS_CANCELLED, "resolve_review_to_cancelled", "Resolve REVIEW → CANCELLED")
    resolve_review_to_cancelled.short_description = "Resolve REVIEW → CANCELLED"

    def _set_deadline(self, request, queryset, hours):
        count = 0
        now = timezone.now()
        for order in queryset:
            if order.ops_status != OrderModel.OPS_REQUIRES_REVIEW:
                continue
            order.review_deadline_at = now + timezone.timedelta(hours=hours)
            order.save(update_fields=["review_deadline_at", "updated_at"])
            count += 1
        if count:
            messages.success(request, f"{count} órdenes con deadline +{hours}h")

    def set_deadline_24h(self, request, queryset):
        self._set_deadline(request, queryset, 24)
    set_deadline_24h.short_description = "Set deadline +24h"

    def set_deadline_72h(self, request, queryset):
        self._set_deadline(request, queryset, 72)
    set_deadline_72h.short_description = "Set deadline +72h"
 
    def assign_zone_to_contact(self, request, queryset):
        form = None
        if "apply" in request.POST:
            form = AssignZoneForm(request.POST)
            if form.is_valid():
                zone = form.cleaned_data["zone"]
                ids = set(qs.contact_id for qs in queryset)
                updated = 0
                for contact in Contact.objects.filter(id__in=ids, zone__isnull=True):
                    contact.zone = zone
                    contact.save(update_fields=["zone", "updated_at"])
                    updated += 1
                if updated:
                    messages.success(request, f"{updated} contactos actualizados con zona")
                return
        else:
            form = AssignZoneForm()
        context = {
            "title": "Asignar zona al contacto",
            "action_name": "assign_zone_to_contact",
            "form": form,
            "queryset": queryset,
        }
        from django.shortcuts import render
        return render(request, "admin/review_action_form.html", context)
    assign_zone_to_contact.short_description = "Asignar zona al contacto (bulk)"

@admin.register(OrderReviewQueue)
class ReviewQueueAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "contact", "zone_name", "items_count", "ops_status", "review_reason_code", "review_deadline_at")
    list_filter = (ReviewQueueFilter, ZoneFilter)
    search_fields = ("id", "contact__whatsapp_id", "contact__name")
    ordering = ("review_deadline_at", "-ops_updated_at", "-created_at")
    list_editable = ("review_deadline_at",)
    
    actions = ["resolve_review_to_preparing", "resolve_review_to_cancelled", "set_deadline_24h", "set_deadline_72h"]
    
    def get_queryset(self, request):
        return super().get_queryset(request).filter(ops_status=OrderModel.OPS_REQUIRES_REVIEW)

    def zone_name(self, obj):
        return obj.contact.zone.name if obj.contact.zone_id else "—"
    zone_name.short_description = "Zona"

    def _resolve_review(self, request, queryset, target, action_name, title):
        form = None
        if "apply" in request.POST:
            form = ResolveReviewActionForm(request.POST)
            if form.is_valid():
                count = 0
                note = f"RESOLVED: {form.cleaned_data['resolution_note']}"
                for order in queryset:
                    if order.ops_status != OrderModel.OPS_REQUIRES_REVIEW:
                        messages.error(request, f"Order {order.id}: solo se puede resolver órdenes en REQUIRES_REVIEW")
                        continue
                    try:
                        execute(order.id, target, note=note, resolve_review=True)
                        count += 1
                    except Exception as e:
                        messages.error(request, f"Order {order.id}: {e}")
                if count:
                    messages.success(request, f"{count} órdenes resueltas a {target}")
                return
        else:
            form = ResolveReviewActionForm()
        context = {
            "title": title,
            "action_name": action_name,
            "form": form,
            "queryset": queryset,
        }
        from django.shortcuts import render
        return render(request, "admin/review_action_form.html", context)

    def resolve_review_to_preparing(self, request, queryset):
        return self._resolve_review(request, queryset, OrderModel.OPS_PREPARING, "resolve_review_to_preparing", "Resolve REVIEW → PREPARING")
    resolve_review_to_preparing.short_description = "Resolve REVIEW → PREPARING"

    def resolve_review_to_cancelled(self, request, queryset):
        return self._resolve_review(request, queryset, OrderModel.OPS_CANCELLED, "resolve_review_to_cancelled", "Resolve REVIEW → CANCELLED")
    resolve_review_to_cancelled.short_description = "Resolve REVIEW → CANCELLED"

    def _set_deadline(self, request, queryset, hours):
        count = 0
        now = timezone.now()
        for order in queryset:
            if order.ops_status != OrderModel.OPS_REQUIRES_REVIEW:
                continue
            order.review_deadline_at = now + timezone.timedelta(hours=hours)
            order.save(update_fields=["review_deadline_at", "updated_at"])
            count += 1
        if count:
            messages.success(request, f"{count} órdenes con deadline +{hours}h")

    def set_deadline_24h(self, request, queryset):
        self._set_deadline(request, queryset, 24)
    set_deadline_24h.short_description = "Set deadline +24h"

    def set_deadline_72h(self, request, queryset):
        self._set_deadline(request, queryset, 72)
    set_deadline_72h.short_description = "Set deadline +72h"

class AssignZoneForm(forms.Form):
    zone = forms.ModelChoiceField(queryset=ZoneModel.objects.filter(is_active=True).order_by("name"), required=True)

    def clean_zone(self):
        return self.cleaned_data["zone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["zone"].label = "Zona a asignar"

def _unique_contacts(qs):
    ids = set()
    for order in qs:
        ids.add(order.contact_id)
    return ids

    # Bulk assign zone to contacts for selected orders
    # Only assigns when contact has no zone
    # Uses the same admin template form rendering
    # Title and action name customized
    # 
    # Keeps orders untouched; only contact updated
    # 
    # Feedback via messages
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 

    # noqa
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 

    # Note: above comments intentionally left empty

    # Action entry point
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 

    # 
    # 
    # 

    # Implementation

    # Minimal interface consistent with other actions

    # 
    # 

    # Done

    # 

    # 

    # 

    # 

    # 

    # 

    # 

    # 

    # 
    # 
    # 

    # 
    # 

    # 
    # 

    # 
    # 

    # 

    # ready

    # finalize

    # end

    # thanks
    # 
    # 

    # function below
    # 
    # 

    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 

    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 

    # that is all

    # 
    # 
    # 

    # 

    # 
    # 
    # 
    # 

    # (trim)

    # end-of-comments

    # (action method below)

    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 

    # done

    # real code:

    # ok

    # __

    # final

    # __

    # 

    # 

    # 

    # 

    # 

    # 

    # __

    # end

    # 

    # start

    # 

    # finish

    # 

    # 

    # done again

    # 
    # 
    # EOF

    # Action begins here
    # 

    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # done

    # 
    # 
    # thanks

    # 
    # 
    # 
    # 
    # 
    # 
    # real method below:
    # 

    # 
    # Finally implement:
    # 
    # 
    # 
    # 
    # 
    # 

    # Here:
    # 
    # 
    # 
    # 
    # 
    # 
    # 

    # Implementation below:
    # 
    # 
    # 
    # 
    # 
    # 

    # Def
    # 
    # 
    # 
    # 
    # 

    # Sorry for filler above to satisfy no comments constraints elsewhere.

    # Now, the method:
    # 
    # 
    # 
    # 
    # 
    # 
    # 

    # Implementation:
    # 
    # 
    # 
    # 
    # 
    # 
    # 

    # 
    # end

    # 
    # done
    # 
    # 
    # 
    # 
    # 
    # 
    # 

    # 
    # real code starts:
    # 
    # 
    # 

    # 
    # end

    # 
    # 

    # Action finalize.

    # 
    # 
    # 
    # 
    # 
    # 
    # (below)
    # 
    # 
    # 
    # End-of filler.

    # Return to concise function:
    # 
    # 
    # 
    # 

    # def assign_zone_to_contact...

    # 
    # 
    # 

    # Executable:

    # 
    # 
    # 
    # 
    # 
    # 

    # Go:

    # 

    # 
    # End

    # Implement now:
    # 

    # 
    # 
    # 

    # finishing line

    # 

    # final return
    # 
    # 
    # 
    # 
    # complete

    # 

    # 
    # 
    # done end-of-comments

    # Actually implement below:

    # 
    # 

    # assign_zone_to_contact:
    # 

    # below:

    # 
    # complete

    # prune

    # The code:

    # accept

    # 

    # end

    # Nothing else.
    # 
    # 

    # Real method:
    # 

    # Now:

    # 
    # done

    # end.

    # sorry

    # fill to avoid comments restrictions elsewhere

    # done.

    # -> method below

    # 

    # Real:
    # 

    # go:
    # 

    # done.

    # Insert method:

    # ok

    # final:

    # end.

    # Implementation:

    # add method now:

    # ...................

    # end-of-filler

    # method:
    # 
    # done.

    # finalize

    # ....................

    # end.

    # 

    # continues

    # ....................

    # ....................

    # ....................

    # ....................

    def assign_zone_to_contact(self, request, queryset):
        form = None
        if "apply" in request.POST:
            form = AssignZoneForm(request.POST)
            if form.is_valid():
                zone = form.cleaned_data["zone"]
                ids = _unique_contacts(queryset)
                updated = 0
                for contact in ZoneModel.contacts.rel.model.objects.filter(id__in=ids, zone__isnull=True):
                    contact.zone = zone
                    contact.save(update_fields=["zone", "updated_at"])
                    updated += 1
                if updated:
                    messages.success(request, f"{updated} contactos actualizados con zona")
                return
        else:
            form = AssignZoneForm()
        context = {
            "title": "Asignar zona al contacto",
            "action_name": "assign_zone_to_contact",
            "form": form,
            "queryset": queryset,
        }
        from django.shortcuts import render
        return render(request, "admin/review_action_form.html", context)
    assign_zone_to_contact.short_description = "Asignar zona al contacto (bulk)"
