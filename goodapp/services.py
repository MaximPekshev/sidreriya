import json
from urllib.parse import urljoin, urlsplit, urlunsplit

from django.conf import settings
from django.db.models import Max
from wishlistapp.services import wishlist_object
from cartapp.services import cart_object
from orderapp.services import popular_order_items
from goodapp.models import Bestseller, Category, Good

def json_goods_list_from_page_object_list(request, page_object_list):
    goods_list = []
    wishlist = wishlist_object(request)
    cart = cart_object(request)
    for item in page_object_list:
        imgObj = item.main_image()
        discount_price = item.discount_price()
        good = {
            'pk': item.pk,
            'slug': item.slug,
            'name': item.name,
            'name_en': item.name_en,
            'quantity': int(item.quantity),
            'price': int(item.price),
            'old_price': int(item.old_price) if item.old_price else None,
            'discount_price': int(discount_price) if discount_price else None,
            'img': imgObj.images.url if imgObj else None, 
            'categoryName': item.category.name if item.category else None,
            'is_vine': item.is_vine,
            'is_cidre': item.is_cidre,
            'in_barrel': item.in_barrel,
            'wl_loading': False,
            'ct_loading': False,
        }
        if wishlist:
            try:
                good['in_wishlist'] = True if item in wishlist.items() else False
            except:
                pass
        try:
            cartinfo = cart.items().get(good=item)
            cart_item_discount_price = cartinfo.discount_price()
            cart_item_discount_summ = cartinfo.discount_summ()
            good['cartInfo'] = {
                'quantity': int(cartinfo.quantity),
                'price': int(cartinfo.price),
                'discount_price': int(cart_item_discount_price) if cart_item_discount_price else None,
                'summ': int(cartinfo.summ),
                'discount_summ': int(cart_item_discount_summ) if cart_item_discount_summ else None
            }
        except:
            pass
        goods_list.append(good)
    return json.dumps(goods_list)

def json_good_from_object(request, good_object):
    wishlist = wishlist_object(request)
    cart = cart_object(request)
    good = {
        'pk': good_object.pk,
        'slug': good_object.slug,
        'name': good_object.name,
        'name_en': good_object.name_en,
        'quantity': int(good_object.quantity),
        'price': int(good_object.price),
        'old_price': int(good_object.old_price) if good_object.old_price else None,
        'discount_price': int(good_object.discount_price()) if good_object.discount_price() else None,
        'img': good_object.main_image().images.url if good_object.main_image() else None, 
        'categoryName': good_object.category.name,
        'is_vine': good_object.is_vine,
        'is_cidre': good_object.is_cidre,
        'in_barrel': good_object.in_barrel,
        'wl_loading': False,
        'ct_loading': False,
    }
    if wishlist:
        try:
            good['in_wishlist'] = True if good_object in wishlist.items() else False
        except:
            pass
    try:
        cartinfo = cart.items().get(good=good_object)
        cart_item_discount_price = cartinfo.discount_price()
        cart_item_discount_summ = cartinfo.discount_summ()
        good['cartInfo'] = {
            'quantity': int(cartinfo.quantity),
            'price': int(cartinfo.price),
            'discount_price': int(cart_item_discount_price) if cart_item_discount_price else None,
            'summ': int(cartinfo.summ),
            'discount_summ': int(cart_item_discount_summ) if cart_item_discount_summ else None
        }
    except:
        pass
    return json.dumps(good)

def set_bestsellers():
    """
    Удаляет старые бестселлеры и создает новые на основе популярных товаров
    """
    for item in Bestseller.objects.all():
        item.delete()
    drinks = popular_order_items().get('drinks')
    dishes = popular_order_items().get('dishes')
    for item in drinks:
        item = Bestseller.objects.create(
            good = drinks[item]['good'],
        )
    for item in dishes:
        item = Bestseller.objects.create(
            good = dishes[item]['good'],
        )


def _absolute_url(base_url: str, path: str) -> str:
    normalized_base = base_url.rstrip("/") + "/"
    normalized_path = path.lstrip("/")
    return urljoin(normalized_base, normalized_path)


def _clean_sitemap_url(url: str) -> str:
    """Return canonical URL for sitemap or empty string if URL has query/fragment."""
    parts = urlsplit(url.strip())
    if not parts.scheme or not parts.netloc:
        return ""
    if parts.query or parts.fragment:
        return ""
    path = parts.path or "/"
    normalized = urlunsplit((parts.scheme, parts.netloc, path, "", ""))
    if path != "/":
        return normalized.rstrip("/") + "/"
    return normalized


def _format_lastmod(dt_obj) -> str | None:
    if not dt_obj:
        return None
    return dt_obj.date().isoformat()


def build_sitemap_xml(
    static_paths: list[str] | None = None,
    base_url: str | None = None,
) -> str:
    """Build sitemap XML from static pages, active categories and active goods.

    Returns raw XML string ready to be saved to file or returned in HTTP response.
    """
    site_url = (base_url or getattr(settings, "SITE_URL", "https://sidreriya.ru")).strip()
    if not site_url:
        site_url = "https://sidreriya.ru"

    static_paths = static_paths or ["/"]

    urls: list[tuple[str, str, str, str | None]] = []

    # Static pages usually change rarely and have higher priority than catalog cards.
    for path in static_paths:
        normalized_path = path.strip()
        if not normalized_path:
            continue
        if not normalized_path.startswith("http://") and not normalized_path.startswith(
            "https://"
        ):
            loc = _absolute_url(site_url, normalized_path)
        else:
            loc = normalized_path
        loc = _clean_sitemap_url(loc)
        if not loc:
            continue
        priority = "1.0" if normalized_path in {"/", ""} else "0.8"
        urls.append((loc, "monthly", priority, None))

    category_history_model = Category.history.model
    categories_lastmod_map = {
        row["id"]: _format_lastmod(row["lastmod"])
        for row in category_history_model.objects.values("id").annotate(
            lastmod=Max("history_date")
        )
    }

    for category in Category.objects.all().order_by("rank", "pk"):
        if not category.slug:
            continue
        loc = _clean_sitemap_url(_absolute_url(site_url, f"catalog/category/{category.slug}/"))
        if not loc:
            continue
        lastmod = categories_lastmod_map.get(category.id)
        urls.append((loc, "weekly", "0.8", lastmod))

    history_model = Good.history.model
    goods_lastmod_map = {
        row["id"]: _format_lastmod(row["lastmod"])
        for row in history_model.objects.values("id").annotate(lastmod=Max("history_date"))
    }

    for good in Good.objects.filter(is_active=True).order_by("pk"):
        if not good.slug:
            continue
        loc = _clean_sitemap_url(_absolute_url(site_url, f"catalog/{good.slug}/"))
        if not loc:
            continue
        lastmod = goods_lastmod_map.get(good.id)
        urls.append((loc, "weekly", "0.7", lastmod))

    unique_urls: list[tuple[str, str, str, str | None]] = []
    seen: set[str] = set()
    for loc, changefreq, priority, lastmod in urls:
        if loc in seen:
            continue
        seen.add(loc)
        unique_urls.append((loc, changefreq, priority, lastmod))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for loc, changefreq, priority, lastmod in unique_urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        if lastmod:
            lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <changefreq>{changefreq}</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")

    return "\n".join(lines) + "\n"