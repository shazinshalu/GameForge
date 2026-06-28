from django.contrib import admin
from django.utils.html import format_html

from .models import Cart, Feedback, User, products, wishlist


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address')
    search_fields = ('name', 'email', 'phone')


@admin.register(products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity', 'image_preview', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'category', 'description')
    readonly_fields = ('image_preview', 'created_at')

    def image_preview(self, obj):
        if obj.has_image:
            return format_html(
                '<img src="{}" style="height: 60px; width: 60px; object-fit: cover; border-radius: 6px;" />',
                obj.image.url,
            )
        return 'No image'

    image_preview.short_description = 'Image'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__name', 'user__email', 'product__name')


@admin.register(wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__name', 'user__email', 'product__name')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('email', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('email', 'feedback_text')
    readonly_fields = ('created_at',)
