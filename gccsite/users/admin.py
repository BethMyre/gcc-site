# Copyright (C) <2019> Association Prologin <association@prologin.org>
# SPDX-License-Identifier: GPL-3.0+

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _


@admin.register(get_user_model())
class GCCUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            _("Profil"),
            {
                'fields': (
                    'gender',
                    'address',
                    'postal_code',
                    'city',
                    'country',
                    'phone',
                    'birthday',
                    'school_stage',
                )
            },
        ),
        (_("Settings"), {'fields': ('allow_mailing', 'timezone')}),
    )
