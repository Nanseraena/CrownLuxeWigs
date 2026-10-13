from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from catalog.models import Category, Collection, Product, ProductVariant, ProductImage, Review
from orders.models import DeliveryMethod
from promotions.models import Coupon
from users.models import Profile, Address

User = get_user_model()

class Command(BaseCommand):
    help = "Seeds database with comprehensive CrownLuxe wig catalog (32+ products, subcategories, collections, variants, and reviews)."

    def handle(self, *args, **options):
        self.stdout.write("Seeding CrownLuxe E-Commerce Store with complete wig catalog...")

        # 1. Superuser / Admin & Customer
        admin_user, _ = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@crownluxe.com", "first_name": "Store", "last_name": "Admin", "is_staff": True, "is_superuser": True}
        )
        if _:
            admin_user.set_password("admin123456")
            admin_user.save()
            Profile.objects.get_or_create(user=admin_user, phone="+256700112233")

        customer_user, _ = User.objects.get_or_create(
            username="nakato_e",
            defaults={"email": "nakato@example.com", "first_name": "Eva", "last_name": "Nakato"}
        )
        if _:
            customer_user.set_password("customer123")
            customer_user.save()
            Profile.objects.get_or_create(user=customer_user, phone="+256772987654")
            Address.objects.get_or_create(
                user=customer_user,
                defaults={
                    "full_name": "Eva Nakato",
                    "phone": "+256772987654",
                    "street_address": "Plot 14 Acacia Avenue, Kololo",
                    "city_or_zone": "Kampala Central",
                    "country": "Uganda",
                    "is_default": True
                }
            )

        # 2. Delivery Methods
        delivery_data = [
            ("Standard Delivery (Kampala Central)", "Kampala Central", Decimal("10000.00"), "Same-day or next day (24 hrs)", 1),
            ("Express Rush Delivery (Kampala Metro)", "Kampala Metro", Decimal("20000.00"), "Within 3-4 hours guaranteed", 2),
            ("Greater Kampala & Wakiso / Entebbe", "Wakiso & Entebbe", Decimal("15000.00"), "1-2 business days", 3),
            ("Upcountry Uganda (Jinja, Mbarara, Gulu, Mbale)", "Upcountry", Decimal("25000.00"), "2-3 business days via courier", 4),
            ("CrownLuxe Boutique Pickup (Acacia Mall)", "Store Pickup", Decimal("0.00"), "Ready in 1 hour (Free)", 5),
        ]
        for name, zone, fee, est, order in delivery_data:
            DeliveryMethod.objects.update_or_create(
                name=name,
                defaults={"zone": zone, "base_fee": fee, "estimated_delivery": est, "sort_order": order, "is_active": True}
            )

        # 3. Coupons
        coupons = [
            ("WELCOME10", "10% Off First Purchase", "percentage", Decimal("10.00"), Decimal("100000.00"), Decimal("150000.00")),
            ("CROWN50K", "50,000 UGX Off High-Value Orders", "fixed", Decimal("50000.00"), Decimal("450000.00"), None),
            ("GLUELESS20", "20% Off Glueless & HD Frontal Wigs", "percentage", Decimal("20.00"), Decimal("200000.00"), Decimal("200000.00")),
            ("VIPCROWN", "15% Off VIP Member Special", "percentage", Decimal("15.00"), Decimal("150000.00"), Decimal("100000.00")),
        ]
        for code, desc, dtype, val, min_o, max_d in coupons:
            Coupon.objects.update_or_create(
                code=code,
                defaults={"description": desc, "discount_type": dtype, "value": val, "min_order_amount": min_o, "max_discount": max_d, "is_active": True}
            )

        # 4. Curated Collections
        collections_data = [
            ("New Arrivals", "new-arrivals", "Fresh luxury additions straight from our master wig makers.", "/images/categories/hd-lace-front.jpg", 1),
            ("Best Sellers", "best-sellers", "Uganda's most-loved virgin hair crowns and viral favorites.", "/images/categories/bone-straight.jpg", 2),
            ("Trending Now", "trending-now", "Pinterest-viral styles, honey blonde balayage, and glass hair.", "/images/categories/colored-highlights.jpg", 3),
            ("Premium Collection", "premium-collection", "Raw cuticle-aligned unprocessed hair with undetectable 0.05mm HD film lace.", "/images/categories/hd-lace-front.jpg", 4),
            ("Everyday Wigs", "everyday-wigs", "Effortless, low maintenance styles made for effortless daily wear.", "/images/categories/glueless-wigs.jpg", 5),
            ("Work & Office Looks", "work-and-office-looks", "Chic blunt bobs and neat sleek silhouettes crafted for business glam.", "/images/categories/bob-wigs.jpg", 6),
            ("Wedding & Special Occasion", "wedding-and-special-occasion", "Showstopping Hollywood waves and ultra-long 30\" frontal crowns.", "/images/categories/deep-wave.jpg", 7),
            ("Beginner-Friendly Wigs", "beginner-friendly-wigs", "Zero glue, zero salon installation needed — slip on in 30 seconds.", "/images/categories/glueless-wigs.jpg", 8),
            ("Affordable Finds", "affordable-finds", "High-style luxury crowns designed for smart, budget-conscious queens.", "/images/categories/bob-wigs.jpg", 9),
            ("Long Hair Collection", "long-hair-collection", "Extra length 24\" to 32\" flowing human hair wigs for maximum drama.", "/images/categories/bone-straight.jpg", 10),
            ("Short Hair Collection", "short-hair-collection", "10\" to 14\" precision bobs, pixies, and breezy short glam.", "/images/categories/bob-wigs.jpg", 11),
        ]
        collection_map = {}
        for cname, cslug, cdesc, cimg, corder in collections_data:
            col, _ = Collection.objects.update_or_create(
                slug=cslug,
                defaults={"name": cname, "description": cdesc, "image_url": cimg, "sort_order": corder, "is_active": True}
            )
            collection_map[cslug] = col
        self.stdout.write(self.style.SUCCESS("Seeded curated collections."))

        # 5. Main Categories & Subcategories
        main_categories = [
            ("Lace Front Wigs", "lace-front-wigs", "Ultra-thin ear-to-ear HD and transparent lace frontals for imperceptible hairline blends.", "/images/categories/hd-lace-front.jpg", 1, [
                ("13x4 Lace Front", "13x4-lace-front"),
                ("13x6 Lace Front", "13x6-lace-front"),
                ("HD Lace Front", "hd-lace-front"),
                ("Transparent Lace Front", "transparent-lace-front"),
                ("Pre-plucked Lace Front", "pre-plucked-lace-front"),
            ]),
            ("Closure Wigs", "closure-wigs", "Low-maintenance HD and Swiss lace closures with realistic natural parting.", "/images/categories/glueless-wigs.jpg", 2, [
                ("4x4 Closure", "4x4-closure"),
                ("5x5 Closure", "5x5-closure"),
                ("2x6 Closure", "2x6-closure"),
                ("2x4 Closure", "2x4-closure"),
            ]),
            ("Glueless Wigs", "glueless-wigs", "Ready-to-wear 3D dome caps with pre-cut lace and silicone security bands. Zero adhesive needed.", "/images/categories/glueless-wigs.jpg", 3, [
                ("Glueless Lace Front", "glueless-lace-front"),
                ("Wear-and-Go Wigs", "wear-and-go-wigs"),
                ("Beginner-Friendly Wigs", "beginner-friendly-category"),
            ]),
            ("Bob Wigs", "bob-wigs", "Chic blunt cut, asymmetrical, and timeless bob styles for everyday glam.", "/images/categories/bob-wigs.jpg", 4, [
                ("Straight Bob", "straight-bob"),
                ("Curly Bob", "curly-bob"),
                ("Wavy Bob", "wavy-bob"),
                ("Layered Bob", "layered-bob"),
            ]),
            ("Curly and Wavy Wigs", "curly-and-wavy-wigs", "Lush bouncy curls, deep waves, water waves, and juicy defined textures.", "/images/categories/deep-wave.jpg", 5, [
                ("Deep Wave", "deep-wave-sub"),
                ("Water Wave", "water-wave-sub"),
                ("Body Wave", "body-wave-sub"),
                ("Loose Wave", "loose-wave-sub"),
                ("Deep Curly", "deep-curly-sub"),
                ("Kinky Curly", "kinky-curly-sub"),
                ("Loose Curly", "loose-curly-sub"),
            ]),
            ("Straight Wigs", "straight-wigs", "Silky, mirror-shine bone straight, yaki, and kinky straight human hair wigs.", "/images/categories/bone-straight.jpg", 6, [
                ("Bone Straight", "bone-straight-sub"),
                ("Silky Straight", "silky-straight-sub"),
                ("Yaki Straight", "yaki-straight-sub"),
                ("Kinky Straight", "kinky-straight-sub"),
            ]),
            ("Colored Wigs", "colored-wigs", "Balayage piano highlights, #613 platinum blonde, #99J burgundy wine, and spiced ginger.", "/images/categories/colored-highlights.jpg", 7, [
                ("Blonde", "blonde-sub"),
                ("Burgundy", "burgundy-sub"),
                ("Ginger", "ginger-sub"),
                ("Chocolate Brown", "chocolate-brown-sub"),
                ("Honey Blonde", "honey-blonde-sub"),
                ("Highlighted", "highlighted-sub"),
                ("Piano Highlights", "piano-highlights-sub"),
                ("Ombre", "ombre-sub"),
                ("Balayage", "balayage-sub"),
            ]),
            ("Specialty Wigs", "specialty-wigs", "Headband slip-on wigs, 360 high-ponytail lace, pixie cuts, and fringe bang styles.", "/images/categories/human-hair.jpg", 8, [
                ("Headband Wigs", "headband-wigs-sub"),
                ("Full Lace Wigs", "full-lace-wigs-sub"),
                ("360 Lace Wigs", "360-lace-wigs-sub"),
                ("Pixie Wigs", "pixie-wigs-sub"),
                ("Bangs and Fringe Wigs", "bangs-and-fringe-wigs-sub"),
            ]),
            ("Hair Extensions", "hair-extensions", "Raw donor virgin human hair bundles, closures, and frontal pieces.", "/images/categories/hair-bundles.jpg", 9, [
                ("Bundles & Closures", "bundles-and-closures"),
                ("Frontal Pieces", "frontal-pieces"),
            ]),
        ]

        cat_map = {}
        subcat_map = {}
        for mname, mslug, mdesc, mimg, morder, subcats in main_categories:
            parent_cat, _ = Category.objects.update_or_create(
                slug=mslug,
                defaults={"name": mname, "description": mdesc, "image_url": mimg, "sort_order": morder, "is_active": True}
            )
            cat_map[mslug] = parent_cat
            for sname, sslug in subcats:
                sub_cat, _ = Category.objects.update_or_create(
                    slug=sslug,
                    defaults={
                        "name": sname,
                        "parent": parent_cat,
                        "description": f"{sname} collection under {mname}.",
                        "image_url": mimg,
                        "is_active": True
                    }
                )
                subcat_map[sslug] = sub_cat

        self.stdout.write(self.style.SUCCESS("Seeded categories and subcategories."))

        # 6. Complete 32+ Product Wig Catalog
        products_data = [
            # --- 1. LACE FRONT WIGS ---
            {
                "name": "CrownLuxe 13x4 HD Lace Bone Straight Frontal Wig",
                "slug": "crownluxe-13x4-hd-bone-straight-frontal-wig",
                "category": "lace-front-wigs", "subcategory": "13x4-lace-front",
                "hair_type": "human", "hair_origin": "brazilian",
                "texture": "Bone Straight", "default_length_inches": 26,
                "default_color": "Natural Black", "default_lace_type": "13x4 HD Invisible Lace",
                "description": "Our signature luxury virgin human hair wig. Featuring ultra-thin transparent HD lace that melts seamlessly into all melanin skin tones. 100% Brazilian virgin hair that flat irons to needle-sleek bone straight with intense natural luster.",
                "is_featured": True, "is_best_seller": True, "is_new_arrival": False,
                "collections": ["best-sellers", "premium-collection", "long-hair-collection"],
                "images": ["/images/categories/bone-straight.jpg"],
                "variants": [
                    {"sku": "CL-BS-18", "length": 18, "color": "Natural Black", "density": "180%", "price": Decimal("520000.00"), "compare_at": Decimal("620000.00"), "stock": 14},
                    {"sku": "CL-BS-22", "length": 22, "color": "Natural Black", "density": "180%", "price": Decimal("650000.00"), "compare_at": Decimal("780000.00"), "stock": 18},
                    {"sku": "CL-BS-26", "length": 26, "color": "Natural Black", "density": "200%", "price": Decimal("820000.00"), "compare_at": Decimal("950000.00"), "stock": 9},
                    {"sku": "CL-BS-30", "length": 30, "color": "Natural Black", "density": "250%", "price": Decimal("980000.00"), "compare_at": Decimal("1150000.00"), "stock": 6},
                    {"sku": "CL-BS-26-JB", "length": 26, "color": "Jet Black", "density": "200%", "price": Decimal("840000.00"), "compare_at": Decimal("970000.00"), "stock": 7},
                ],
                "reviews": [("Sarah K.", 5, "Unbelievable melt!", "The HD lace vanished completely against my scalp. Best straight wig in Kampala."), ("Brenda N.", 5, "Glass hair perfection", "Combed effortlessly with no tangles. Delivered in 2 hours to Kololo.")]
            },
            {
                "name": "Luxe Deep Wave 13x6 Melted Frontal Wig",
                "slug": "luxe-deep-wave-13x6-melted-frontal-wig",
                "category": "lace-front-wigs", "subcategory": "13x6-lace-front",
                "hair_type": "human", "hair_origin": "peruvian",
                "texture": "Deep Wave", "default_length_inches": 24,
                "default_color": "Natural Black", "default_lace_type": "13x6 Melted HD Swiss Lace",
                "description": "Lush, bouncy, hydrated deep wave curls with deep 6-inch parting versatility. Allows half-up half-down and high ponytail styling with baby hairs.",
                "is_featured": True, "is_best_seller": True, "is_new_arrival": False,
                "collections": ["best-sellers", "wedding-and-special-occasion", "long-hair-collection"],
                "images": ["/images/categories/deep-wave.jpg"],
                "variants": [
                    {"sku": "CL-DW-20", "length": 20, "color": "Natural Black", "density": "180%", "price": Decimal("610000.00"), "compare_at": Decimal("720000.00"), "stock": 10},
                    {"sku": "CL-DW-24", "length": 24, "color": "Natural Black", "density": "200%", "price": Decimal("760000.00"), "compare_at": Decimal("890000.00"), "stock": 15},
                    {"sku": "CL-DW-28", "length": 28, "color": "Natural Black", "density": "250%", "price": Decimal("940000.00"), "compare_at": Decimal("1100000.00"), "stock": 8},
                ],
                "reviews": [("Patricia M.", 5, "Juicy curls!", "Defined spirals that spring back after washing. Zero frizz in Kampala humidity.")]
            },
            {
                "name": "CrownLuxe Pre-Plucked Body Wave Invisible Swiss Lace Frontal",
                "slug": "crownluxe-pre-plucked-body-wave-invisible-swiss-lace-frontal",
                "category": "lace-front-wigs", "subcategory": "pre-plucked-lace-front",
                "hair_type": "human", "hair_origin": "malaysian",
                "texture": "Body Wave", "default_length_inches": 28,
                "default_color": "Natural Black", "default_lace_type": "13x6 Real Skin Melt HD Film Lace",
                "description": "Hollywood glam body wave wig with pre-customized single-knot hairline and delicate temple baby hairs. Melts into any undertone effortlessly.",
                "is_featured": True, "is_best_seller": False, "is_new_arrival": True,
                "collections": ["new-arrivals", "premium-collection", "wedding-and-special-occasion"],
                "images": ["/images/categories/hd-lace-front.jpg"],
                "variants": [
                    {"sku": "CL-BW-22", "length": 22, "color": "Natural Black", "density": "180%", "price": Decimal("680000.00"), "compare_at": Decimal("800000.00"), "stock": 8},
                    {"sku": "CL-BW-28", "length": 28, "color": "Natural Black", "density": "200%", "price": Decimal("890000.00"), "compare_at": Decimal("1050000.00"), "stock": 12},
                    {"sku": "CL-BW-32", "length": 32, "color": "Natural Black", "density": "250%", "price": Decimal("1150000.00"), "compare_at": Decimal("1350000.00"), "stock": 5},
                ],
                "reviews": [("Grace T.", 5, "Met Gala waves", "Pure royalty hair. Got endless compliments at my friend's wedding in Entebbe.")]
            },
            {
                "name": "CrownLuxe Transparent 13x4 Kinky Straight Frontal Wig",
                "slug": "crownluxe-transparent-13x4-kinky-straight-frontal-wig",
                "category": "lace-front-wigs", "subcategory": "transparent-lace-front",
                "hair_type": "human", "hair_origin": "vietnamese",
                "texture": "Kinky Straight", "default_length_inches": 22,
                "default_color": "Natural Black", "default_lace_type": "13x4 Transparent Swiss Lace",
                "description": "Mimics a fresh silk press on coarse 4C natural hair. Full-bodied volume with a natural textured look that blends invisibly with natural edges.",
                "is_featured": False, "is_best_seller": False, "is_new_arrival": True,
                "collections": ["new-arrivals", "everyday-wigs"],
                "images": ["/images/categories/bone-straight.jpg"],
                "variants": [
                    {"sku": "CL-KS-18", "length": 18, "color": "Natural Black", "density": "180%", "price": Decimal("560000.00"), "compare_at": Decimal("680000.00"), "stock": 10},
                    {"sku": "CL-KS-22", "length": 22, "color": "Natural Black", "density": "200%", "price": Decimal("690000.00"), "compare_at": Decimal("820000.00"), "stock": 7},
                ],
                "reviews": [("Doreen A.", 5, "Looks like my real hair", "People genuinely thought I had blown out my own hair. In love!")]
            },

            # --- 2. CLOSURE WIGS ---
            {
                "name": "CrownLuxe 5x5 HD Closure Water Wave Wig",
                "slug": "crownluxe-5x5-hd-closure-water-wave-wig",
                "category": "closure-wigs", "subcategory": "5x5-closure",
                "hair_type": "human", "hair_origin": "brazilian",
                "texture": "Water Wave", "default_length_inches": 22,
                "default_color": "Natural Black", "default_lace_type": "5x5 HD Swiss Lace Closure",
                "description": "Effortless, low maintenance 5x5 HD closure with wet-and-wavy high elasticity coils. Clean free-parting space with zero glue needed on the sides.",
                "is_featured": False, "is_best_seller": True, "is_new_arrival": False,
                "collections": ["best-sellers", "everyday-wigs", "beginner-friendly-wigs"],
                "images": ["/images/categories/deep-wave.jpg"],
                "variants": [
                    {"sku": "CL-WW-18", "length": 18, "color": "Natural Black", "density": "180%", "price": Decimal("490000.00"), "compare_at": Decimal("590000.00"), "stock": 16},
                    {"sku": "CL-WW-22", "length": 22, "color": "Natural Black", "density": "180%", "price": Decimal("620000.00"), "compare_at": Decimal("740000.00"), "stock": 11},
                    {"sku": "CL-WW-26", "length": 26, "color": "Natural Black", "density": "200%", "price": Decimal("780000.00"), "compare_at": Decimal("920000.00"), "stock": 8},
                ],
                "reviews": [("Juliet K.", 5, "My daily go-to", "Put some mousse and water and I'm ready to leave the house in 2 minutes.")]
            },
            {
                "name": "CrownLuxe 4x4 Pre-Cut Glueless Silky Straight Closure Wig",
                "slug": "crownluxe-4x4-pre-cut-glueless-silky-straight-closure-wig",
                "category": "closure-wigs", "subcategory": "4x4-closure",
                "hair_type": "human", "hair_origin": "indian",
                "texture": "Silky Straight", "default_length_inches": 18,
                "default_color": "Natural Black", "default_lace_type": "4x4 Pre-Cut Swiss Lace",
                "description": "Perfect beginner closure wig. 100% Indian virgin temple hair with natural softness and mirror luster. Pre-plucked with pre-cut lace.",
                "is_featured": False, "is_best_seller": False, "is_new_arrival": False,
                "collections": ["affordable-finds", "beginner-friendly-wigs", "work-and-office-looks"],
                "images": ["/images/categories/bone-straight.jpg"],
                "variants": [
                    {"sku": "CL-SS-14", "length": 14, "color": "Natural Black", "density": "150%", "price": Decimal("390000.00"), "compare_at": Decimal("480000.00"), "stock": 14},
                    {"sku": "CL-SS-18", "length": 18, "color": "Natural Black", "density": "180%", "price": Decimal("490000.00"), "compare_at": Decimal("590000.00"), "stock": 9},
                ],
                "reviews": [("Mercy N.", 5, "Very affordable and great quality", "High grade virgin hair for under 400k. Excellent purchase.")]
            },
            {
                "name": "CrownLuxe 2x6 Deep Middle Part Closure Wig",
                "slug": "crownluxe-2x6-deep-middle-part-closure-wig",
                "category": "closure-wigs", "subcategory": "2x6-closure",
                "hair_type": "human", "hair_origin": "cambodian",
                "texture": "Bone Straight", "default_length_inches": 24,
                "default_color": "Natural Black", "default_lace_type": "2x6 Kim K HD Lace Closure",
                "description": "Viral 2x6 'Kim K' deep parting closure unit. Provides an ultra-deep 6-inch natural middle scalp part with zero temple lace to cut or melt.",
                "is_featured": False, "is_best_seller": False, "is_new_arrival": True,
                "collections": ["new-arrivals", "everyday-wigs"],
                "images": ["/images/categories/bone-straight.jpg"],
                "variants": [
                    {"sku": "CL-2X6-20", "length": 20, "color": "Natural Black", "density": "180%", "price": Decimal("550000.00"), "compare_at": Decimal("660000.00"), "stock": 8},
                    {"sku": "CL-2X6-24", "length": 24, "color": "Natural Black", "density": "200%", "price": Decimal("680000.00"), "compare_at": Decimal("810000.00"), "stock": 6},
                ],
                "reviews": [("Fiona M.", 5, "Cleanest parting ever", "The 6-inch depth goes all the way back. Looks like a salon middle part.")]
            },

            # --- 3. GLUELESS WIGS ---
            {
                "name": "CrownLuxe 3D Dome Cap Wear & Go Body Wave Wig",
                "slug": "crownluxe-3d-dome-cap-wear-go-body-wave-wig",
                "category": "glueless-wigs", "subcategory": "wear-and-go-wigs",
                "hair_type": "human", "hair_origin": "brazilian",
                "texture": "Body Wave", "default_length_inches": 22,
                "default_color": "Natural Black", "default_lace_type": "7x5 Bye-Bye Knots 3D Dome Glueless HD Lace",
                "description": "Slip on in 30 seconds. Features pre-cut zig-zag scalloped lace, pre-bleached invisible knots, and an anti-slip silicone elastic band. Zero adhesive needed.",
                "is_featured": True, "is_best_seller": True, "is_new_arrival": False,
                "collections": ["best-sellers", "beginner-friendly-wigs", "everyday-wigs"],
                "images": ["/images/categories/glueless-wigs.jpg"],
                "variants": [
                    {"sku": "CL-WG-16", "length": 16, "color": "Natural Black", "density": "180%", "price": Decimal("460000.00"), "compare_at": Decimal("560000.00"), "stock": 15},
                    {"sku": "CL-WG-20", "length": 20, "color": "Natural Black", "density": "180%", "price": Decimal("590000.00"), "compare_at": Decimal("710000.00"), "stock": 20},
                    {"sku": "CL-WG-24", "length": 24, "color": "Natural Black", "density": "200%", "price": Decimal("740000.00"), "compare_at": Decimal("880000.00"), "stock": 10},
                ],
                "reviews": [("Eva N.", 5, "Life saver for busy mornings", "I literally take it out the box, put it on, and I'm ready for court in 30 seconds.")]
            },
            {
                "name": "CrownLuxe Bye-Bye Knots Glueless Straight Wig",
                "slug": "crownluxe-bye-bye-knots-glueless-straight-wig",
                "category": "glueless-wigs", "subcategory": "glueless-lace-front",
                "hair_type": "human", "hair_origin": "peruvian",
                "texture": "Bone Straight", "default_length_inches": 20,
                "default_color": "Natural Black", "default_lace_type": "Pre-cut 7x5 Glueless HD Lace",
                "description": "Zero gel, zero glue, zero bleached knot irritation. High density bone straight virgin hair with snug, comfortable cap grip.",
                "is_featured": False, "is_best_seller": False, "is_new_arrival": True,
                "collections": ["new-arrivals", "beginner-friendly-wigs"],
                "images": ["/images/categories/glueless-wigs.jpg"],
                "variants": [
                    {"sku": "CL-BBK-18", "length": 18, "color": "Natural Black", "density": "180%", "price": Decimal("530000.00"), "compare_at": Decimal("640000.00"), "stock": 11},
                    {"sku": "CL-BBK-22", "length": 22, "color": "Natural Black", "density": "200%", "price": Decimal("670000.00"), "compare_at": Decimal("800000.00"), "stock": 8},
                ],
                "reviews": [("Ritah B.", 5, "No more glue headaches", "My edges are so happy. Holds tight even when it's windy.")]
            },
            {
                "name": "CrownLuxe Beginner-Friendly 30-Second Throw-On Bob",
                "slug": "crownluxe-beginner-friendly-30-second-throw-on-bob",
                "category": "glueless-wigs", "subcategory": "beginner-friendly-category",
                "hair_type": "human", "hair_origin": "brazilian",
                "texture": "Straight Bob", "default_length_inches": 12,
                "default_color": "Natural Black", "default_lace_type": "4x4 Pre-Cut Glueless Lace",
                "description": "The easiest wig you will ever own. A chic 12-inch bob cut with pre-customized hairline. Just shake, slip on, and go.",
                "is_featured": False, "is_best_seller": True, "is_new_arrival": False,
                "collections": ["best-sellers", "beginner-friendly-wigs", "short-hair-collection", "work-and-office-looks"],
                "images": ["/images/categories/bob-wigs.jpg"],
                "variants": [
                    {"sku": "CL-BOB-10-GL", "length": 10, "color": "Natural Black", "density": "150%", "price": Decimal("380000.00"), "compare_at": Decimal("470000.00"), "stock": 12},
                    {"sku": "CL-BOB-12-GL", "length": 12, "color": "Natural Black", "density": "180%", "price": Decimal("440000.00"), "compare_at": Decimal("530000.00"), "stock": 18},
                ],
                "reviews": [("Claire W.", 5, "Worth every shilling", "Got this as my first ever wig. Very easy to maintain.")]
            },

            # --- 4. BOB WIGS ---
            {
                "name": "CrownLuxe 10\" Precision Blunt Cut Sleek Bob",
                "slug": "crownluxe-10-precision-blunt-cut-sleek-bob",
                "category": "bob-wigs", "subcategory": "straight-bob",
                "hair_type": "human", "hair_origin": "brazilian",
                "texture": "Straight Bob", "default_length_inches": 10,
                "default_color": "Natural Brown", "default_lace_type": "5x5 Pre-Cut HD Closure Lace",
                "description": "Razor-sharp blunt cut precision bob in rich chocolate espresso tone. Lightweight, breezy around the neck, with razor-sharp ends.",
                "is_featured": True, "is_best_seller": True, "is_new_arrival": False,
                "collections": ["best-sellers", "work-and-office-looks", "short-hair-collection"],
                "images": ["/images/categories/bob-wigs.jpg"],
                "variants": [
                    {"sku": "CL-BLUNT-10-BR", "length": 10, "color": "Natural Brown", "density": "150%", "price": Decimal("410000.00"), "compare_at": Decimal("500000.00"), "stock": 10},
                    {"sku": "CL-BLUNT-10-BK", "length": 10, "color": "Natural Black", "density": "150%", "price": Decimal("410000.00"), "compare_at": Decimal("500000.00"), "stock": 14},
                    {"sku": "CL-BLUNT-12-BK", "length": 12, "color": "Natural Black", "density": "180%", "price": Decimal("460000.00"), "compare_at": Decimal("560000.00"), "stock": 12},
                ],
                "reviews": [("Agnes N.", 5, "Sharp and chic!", "The blunt ends are perfection. Looks like I walked out of a luxury Paris salon.")]
            },
            {
                "name": "CrownLuxe 12\" Asymmetrical Chic Bone Straight Bob",
                "slug": "crownluxe-12-asymmetrical-chic-bone-straight-bob",
                "category": "bob-wigs", "subcategory": "straight-bob",
                "hair_type": "human", "hair_origin": "peruvian",
                "texture": "Bone Straight", "default_length_inches": 12,
                "default_color": "Natural Black", "default_lace_type": "13x4 HD Frontal Lace",
                "description": "Dramatic high-fashion asymmetrical cut with longer sleek face-framing front and tapered back neck profile.",
                "is_featured": False, "is_best_seller": False, "is_new_arrival": True,
                "collections": ["new-arrivals", "work-and-office-looks", "short-hair-collection"],
                "images": ["/images/categories/bob-wigs.jpg"],
                "variants": [
                    {"sku": "CL-ASYM-12", "length": 12, "color": "Natural Black", "density": "180%", "price": Decimal("480000.00"), "compare_at": Decimal("580000.00"), "stock": 8},
                    {"sku": "CL-ASYM-14", "length": 14, "color": "Natural Black", "density": "180%", "price": Decimal("530000.00"), "compare_at": Decimal("630000.00"), "stock": 6},
                ],
                "reviews": [("Rachel A.", 5, "Boss energy", "Wore this to a boardroom meeting and received so many compliments.")]
            },
            {
                "name": "CrownLuxe 14\" Deep Wave Curly Bob with Fringe Bangs",
                "slug": "crownluxe-14-deep-wave-curly-bob-with-fringe-bangs",
                "category": "bob-wigs", "subcategory": "curly-bob",
                "hair_type": "human", "hair_origin": "malaysian",
                "texture": "Deep Wave", "default_length_inches": 14,
                "default_color": "Natural Black", "default_lace_type": "Glueless Cap with French Bangs",
                "description": "Bouncy voluminous curls framed with cute wispy fringe bangs. No lace installation needed whatsoever.",
                "is_featured": False, "is_best_seller": False, "is_new_arrival": False,
                "collections": ["everyday-wigs", "short-hair-collection", "affordable-finds"],
                "images": ["/images/categories/deep-wave.jpg"],
                "variants": [
                    {"sku": "CL-CBOB-12", "length": 12, "color": "Natural Black", "density": "180%", "price": Decimal("420000.00"), "compare_at": Decimal("510000.00"), "stock": 10},
                    {"sku": "CL-CBOB-14", "length": 14, "color": "Natural Black", "density": "180%", "price": Decimal("470000.00"), "compare_at": Decimal("570000.00"), "stock": 7},
                ],
                "reviews": [("Sharon K.", 5, "Cute and playful", "The curls have so much bounce and the bangs fall right on the eyebrows.")]
            },
            {
                "name": "CrownLuxe 10\" Layered Side-Part Bob in Chocolate Brown",
                "slug": "crownluxe-10-layered-side-part-bob-in-chocolate-brown",
                "category": "bob-wigs", "subcategory": "layered-bob",
                "hair_type": "human", "hair_origin": "indian",
                "texture": "Straight Bob", "default_length_inches": 10,
                "default_color": "Chocolate Brown", "default_lace_type": "5x5 HD Closure",
                "description": "Rich mocha #4 chocolate brown with soft feather layers that swoop elegantly behind the ears.",
                "is_featured": False, "is_best_seller": False, "is_new_arrival": True,
                "collections": ["new-arrivals", "work-and-office-looks", "short-hair-collection"],
                "images": ["/images/categories/bob-wigs.jpg"],
                "variants": [
                    {"sku": "CL-LBOB-10", "length": 10, "color": "Chocolate Brown", "density": "150%", "price": Decimal("440000.00"), "compare_at": Decimal("530000.00"), "stock": 9},
                ],
                "reviews": [("Hellen O.", 5, "The color is gorgeous", "Not too dark, not too bright. Exactly like chocolate truffle.")]
            },

            # --- 5. CURLY AND WAVY WIGS ---
            {
                "name": "CrownLuxe 28\" Water Wave High-Definition Curls",
                "slug": "crownluxe-28-water-wave-high-definition-curls",
                "category": "curly-and-wavy-wigs", "subcategory": "water-wave-sub",
                "hair_type": "human", "hair_origin": "peruvian",
                "texture": "Water Wave", "default_length_inches": 28,
                "default_color": "Natural Black", "default_lace_type": "13x4 HD Transparent Lace Front",
                "description": "Ultra-long mermaid coils with glistening water ripples. 200% density providing dramatic, full-bodied volume from roots to tips.",
                "is_featured": True, "is_best_seller": False, "is_new_arrival": True,
                "collections": ["new-arrivals", "long-hair-collection", "wedding-and-special-occasion"],
                "images": ["/images/categories/deep-wave.jpg"],
                "variants": [
                    {"sku": "CL-WW28-24", "length": 24, "color": "Natural Black", "density": "200%", "price": Decimal("770000.00"), "compare_at": Decimal("910000.00"), "stock": 10},
                    {"sku": "CL-WW28-28", "length": 28, "color": "Natural Black", "density": "200%", "price": Decimal("920000.00"), "compare_at": Decimal("1080000.00"), "stock": 8},
                    {"sku": "CL-WW28-32", "length": 32, "color": "Natural Black", "density": "250%", "price": Decimal("1120000.00"), "compare_at": Decimal("1320000.00"), "stock": 4},
                ],
                "reviews": [("Lillian B.", 5, "Mermaid queen vibe", "Reached all the way down to my waist. Softest water wave ever.")]
            },
            {
                "name": "CrownLuxe 24\" Loose Wave Mermaid Luster Wig",
                "slug": "crownluxe-24-loose-wave-mermaid-luster-wig",
                "category": "curly-and-wavy-wigs", "subcategory": "loose-wave-sub",
                "hair_type": "human", "hair_origin": "indian",
                "texture": "Loose Wave", "default_length_inches": 24,
                "default_color": "Natural Black", "default_lace_type": "13x4 Invisible HD Lace",
                "description": "Large, cascading S-pattern waves that hold their shape for days. Silky soft virgin Indian hair with high elasticity.",
                "is_featured": False, "is_best_seller": False, "is_new_arrival": False,
                "collections": ["everyday-wigs", "long-hair-collection"],
                "images": ["/images/categories/hd-lace-front.jpg"],
                "variants": [
                    {"sku": "CL-LW-20", "length": 20, "color": "Natural Black", "density": "180%", "price": Decimal("580000.00"), "compare_at": Decimal("690000.00"), "stock": 11},
                    {"sku": "CL-LW-24", "length": 24, "color": "Natural Black", "density": "200%", "price": Decimal("730000.00"), "compare_at": Decimal("860000.00"), "stock": 7},
                ],
                "reviews": [("Joan A.", 5, "Effortless waves", "Brushes through like a dream and doesn't shed.")]
            },
            {
                "name": "CrownLuxe 22\" Kinky Curly 4C Scalp-Blended Natural Wig",
                "slug": "crownluxe-22-kinky-curly-4c-scalp-blended-natural-wig",
                "category": "curly-and-wavy-wigs", "subcategory": "kinky-curly-sub",
                "hair_type": "human", "hair_origin": "vietnamese",
                "texture": "Kinky Curly", "default_length_inches": 22,
                "default_color": "Natural Black", "default_lace_type": "13x4 HD Frontal with Natural Hairline",
                "description": "Celebrates natural afro textures. Dense, corkscrew micro-curls that mimic healthy 4B/4C coils with realistic scalp emergence.",
                "is_featured": False, "is_best_seller": True, "is_new_arrival": False,
                "collections": ["best-sellers", "everyday-wigs"],
                "images": ["/images/categories/deep-wave.jpg"],
                "variants": [
                    {"sku": "CL-KC-16", "length": 16, "color": "Natural Black", "density": "200%", "price": Decimal("520000.00"), "compare_at": Decimal("620000.00"), "stock": 12},
                    {"sku": "CL-KC-22", "length": 22, "color": "Natural Black", "density": "200%", "price": Decimal("690000.00"), "compare_at": Decimal("820000.00"), "stock": 9},
                ],
                "reviews": [("Anita M.", 5, "My holy grail", "Looks identical to my natural hair when it's well moisturized.")]
            },
            {
                "name": "CrownLuxe 26\" Raw Cambodian Deep Curly Wig",
                "slug": "crownluxe-26-raw-cambodian-deep-curly-wig",
                "category": "curly-and-wavy-wigs", "subcategory": "deep-curly-sub",
                "hair_type": "human", "hair_origin": "cambodian",
                "texture": "Deep Curly", "default_length_inches": 26,
                "default_color": "Natural Black", "default_lace_type": "13x6 HD Swiss Lace Frontal",
                "description": "Raw donor Cambodian hair. Coarser strands with thick cuticle layers that create monumental volume and defined curls.",
                "is_featured": True, "is_best_seller": False, "is_new_arrival": True,
                "collections": ["new-arrivals", "premium-collection", "long-hair-collection"],
                "images": ["/images/categories/deep-wave.jpg"],
                "variants": [
                    {"sku": "CL-CAM-22", "length": 22, "color": "Natural Black", "density": "200%", "price": Decimal("760000.00"), "compare_at": Decimal("900000.00"), "stock": 6},
                    {"sku": "CL-CAM-26", "length": 26, "color": "Natural Black", "density": "250%", "price": Decimal("940000.00"), "compare_at": Decimal("1110000.00"), "stock": 4},
                ],
                "reviews": [("Winnie T.", 5, "Thick and luxurious", "This hair is for people who love big, bold, luxurious volume.")]
            },

            # --- 6. STRAIGHT WIGS ---
            {
                "name": "CrownLuxe 30\" Glass Finish Bone Straight Virgin Wig",
                "slug": "crownluxe-30-glass-finish-bone-straight-virgin-wig",
                "category": "straight-wigs", "subcategory": "bone-straight-sub",
                "hair_type": "human", "hair_origin": "brazilian",
                "texture": "Bone Straight", "default_length_inches": 30,
                "default_color": "Natural Black", "default_lace_type": "13x4 HD Invisible Swiss Lace",
                "description": "The viral Pinterest 'Glass Hair'. Straight down to the tailbone with needle-sharp blunt ends and liquid mirror shine.",
                "is_featured": True, "is_best_seller": True, "is_new_arrival": False,
                "collections": ["best-sellers", "premium-collection", "long-hair-collection"],
                "images": ["/images/categories/bone-straight.jpg"],
                "variants": [
                    {"sku": "CL-GLASS-26", "length": 26, "color": "Natural Black", "density": "200%", "price": Decimal("840000.00"), "compare_at": Decimal("980000.00"), "stock": 10},
                    {"sku": "CL-GLASS-30", "length": 30, "color": "Natural Black", "density": "250%", "price": Decimal("1020000.00"), "compare_at": Decimal("1200000.00"), "stock": 6},
                    {"sku": "CL-GLASS-30-JB", "length": 30, "color": "Jet Black", "density": "250%", "price": Decimal("1040000.00"), "compare_at": Decimal("1220000.00"), "stock": 5},
                ],
                "reviews": [("Florence N.", 5, "Showstopper", "Turned heads everywhere I went. The hair moves like liquid silk.")]
            },
            {
                "name": "CrownLuxe 28\" Yaki Straight Textured Blowout Wig",
                "slug": "crownluxe-28-yaki-straight-textured-blowout-wig",
                "category": "straight-wigs", "subcategory": "yaki-straight-sub",
                "hair_type": "human", "hair_origin": "peruvian",
                "texture": "Yaki Straight", "default_length_inches": 28,
                "default_color": "Natural Black", "default_lace_type": "13x4 Transparent Frontal",
                "description": "The look of freshly blown-out relaxed hair. Has micro-crimps that give tremendous body and hold curls much longer than silky hair.",
                "is_featured": False, "is_best_seller": False, "is_new_arrival": False,
                "collections": ["everyday-wigs", "long-hair-collection"],
                "images": ["/images/categories/bone-straight.jpg"],
                "variants": [
                    {"sku": "CL-YAKI-22", "length": 22, "color": "Natural Black", "density": "180%", "price": Decimal("640000.00"), "compare_at": Decimal("760000.00"), "stock": 8},
                    {"sku": "CL-YAKI-28", "length": 28, "color": "Natural Black", "density": "200%", "price": Decimal("830000.00"), "compare_at": Decimal("980000.00"), "stock": 6},
                ],
                "reviews": [("Priscilla E.", 5, "Hold curls for 3 days", "Wand curled it once and the curls held throughout the weekend!")]
            },
            {
                "name": "CrownLuxe 24\" Silky Straight Raw Burmese Donor Wig",
                "slug": "crownluxe-24-silky-straight-raw-burmese-donor-wig",
                "category": "straight-wigs", "subcategory": "silky-straight-sub",
                "hair_type": "human", "hair_origin": "other",
                "texture": "Silky Straight", "default_length_inches": 24,
                "default_color": "Natural Brown", "default_lace_type": "5x5 HD Closure",
                "description": "Raw donor Burmese human hair with natural warm undertones. Thick cuticle alignment that bleaches to 613 blonde easily.",
                "is_featured": False, "is_best_seller": False, "is_new_arrival": True,
                "collections": ["new-arrivals", "premium-collection"],
                "images": ["/images/categories/human-hair.jpg"],
                "variants": [
                    {"sku": "CL-BURM-20", "length": 20, "color": "Natural Brown", "density": "180%", "price": Decimal("660000.00"), "compare_at": Decimal("780000.00"), "stock": 7},
                    {"sku": "CL-BURM-24", "length": 24, "color": "Natural Brown", "density": "200%", "price": Decimal("810000.00"), "compare_at": Decimal("950000.00"), "stock": 5},
                ],
                "reviews": [("Naomi K.", 5, "Top grade raw hair", "You can tell this is pure single-donor hair. Feels so healthy.")]
            },

            # --- 7. COLORED WIGS ---
            {
                "name": "CrownLuxe P4/27 Piano Honey Blonde Balayage Wig",
                "slug": "crownluxe-p4-27-piano-honey-blonde-balayage-wig",
                "category": "colored-wigs", "subcategory": "piano-highlights-sub",
                "hair_type": "human", "hair_origin": "brazilian",
                "texture": "Body Wave", "default_length_inches": 24,
                "default_color": "Piano Highlights", "default_lace_type": "13x4 HD Transparent Frontal",
                "description": "The viral Pinterest honey blonde piano highlight trend. Alternating caramel honey blonde ribbons and dark chocolate brown streaks.",
                "is_featured": True, "is_best_seller": True, "is_new_arrival": False,
                "collections": ["trending-now", "best-sellers", "wedding-and-special-occasion", "long-hair-collection"],
                "images": ["/images/categories/colored-highlights.jpg"],
                "variants": [
                    {"sku": "CL-P427-20", "length": 20, "color": "Piano Highlights", "density": "180%", "price": Decimal("690000.00"), "compare_at": Decimal("820000.00"), "stock": 14},
                    {"sku": "CL-P427-24", "length": 24, "color": "Piano Highlights", "density": "200%", "price": Decimal("840000.00"), "compare_at": Decimal("990000.00"), "stock": 12},
                    {"sku": "CL-P427-28", "length": 28, "color": "Piano Highlights", "density": "250%", "price": Decimal("1030000.00"), "compare_at": Decimal("1220000.00"), "stock": 6},
                ],
                "reviews": [("Rebecca K.", 5, "Pinterest dream come true", "The blend of honey blonde and mocha brown is so flattering on dark skin.")]
            },
            {
                "name": "CrownLuxe #350 Spiced Ginger Copper Loose Wave Wig",
                "slug": "crownluxe-350-spiced-ginger-copper-loose-wave-wig",
                "category": "colored-wigs", "subcategory": "ginger-sub",
                "hair_type": "human", "hair_origin": "peruvian",
                "texture": "Loose Wave", "default_length_inches": 22,
                "default_color": "Ginger", "default_lace_type": "13x4 HD Lace Frontal",
                "description": "Warm cinnamon spice and vibrant copper ginger tones that give an intoxicating sunlit glow. Pre-toned and deeply conditioned.",
                "is_featured": True, "is_best_seller": False, "is_new_arrival": True,
                "collections": ["trending-now", "new-arrivals", "wedding-and-special-occasion"],
                "images": ["/images/categories/colored-highlights.jpg"],
                "variants": [
                    {"sku": "CL-GIN-18", "length": 18, "color": "Ginger", "density": "180%", "price": Decimal("620000.00"), "compare_at": Decimal("740000.00"), "stock": 9},
                    {"sku": "CL-GIN-22", "length": 22, "color": "Ginger", "density": "200%", "price": Decimal("780000.00"), "compare_at": Decimal("920000.00"), "stock": 8},
                    {"sku": "CL-COP-22", "length": 22, "color": "Copper", "density": "200%", "price": Decimal("780000.00"), "compare_at": Decimal("920000.00"), "stock": 5},
                ],
                "reviews": [("Faith N.", 5, "Obsessed with this ginger!", "The color is so rich. Doesn't fade or dry out.")]
            },
            {
                "name": "CrownLuxe #99J Deep Wine Burgundy Bone Straight Wig",
                "slug": "crownluxe-99j-deep-wine-burgundy-bone-straight-wig",
                "category": "colored-wigs", "subcategory": "burgundy-sub",
                "hair_type": "human", "hair_origin": "brazilian",
                "texture": "Bone Straight", "default_length_inches": 24,
                "default_color": "Burgundy", "default_lace_type": "13x4 HD Transparent Frontal",
                "description": "Vampy, luxurious 99J deep cherry wine that shimmers with dark burgundy red undertones in direct sunlight.",
                "is_featured": False, "is_best_seller": True, "is_new_arrival": False,
                "collections": ["trending-now", "best-sellers", "long-hair-collection"],
                "images": ["/images/categories/colored-highlights.jpg"],
                "variants": [
                    {"sku": "CL-99J-20", "length": 20, "color": "Burgundy", "density": "180%", "price": Decimal("660000.00"), "compare_at": Decimal("780000.00"), "stock": 10},
                    {"sku": "CL-99J-24", "length": 24, "color": "Burgundy", "density": "200%", "price": Decimal("820000.00"), "compare_at": Decimal("970000.00"), "stock": 7},
                ],
                "reviews": [("Miriam L.", 5, "Rich cherry color", "So chic for evening events. Bone straight with zero flyaways.")]
            },
            {
                "name": "CrownLuxe #613 Russian Virgin Platinum Ice Blonde Wig",
                "slug": "crownluxe-613-russian-virgin-platinum-ice-blonde-wig",
                "category": "colored-wigs", "subcategory": "blonde-sub",
                "hair_type": "human", "hair_origin": "other",
                "texture": "Bone Straight", "default_length_inches": 26,
                "default_color": "Platinum Blonde", "default_lace_type": "13x4 Transparent HD Lace",
                "description": "Bleached to lightest #613 ice blonde from raw virgin donor hair. Soft, silky, and ready to wear or dye into custom pastels.",
                "is_featured": True, "is_best_seller": False, "is_new_arrival": True,
                "collections": ["trending-now", "new-arrivals", "premium-collection"],
                "images": ["/images/categories/colored-highlights.jpg"],
                "variants": [
                    {"sku": "CL-613-22", "length": 22, "color": "Platinum Blonde", "density": "180%", "price": Decimal("790000.00"), "compare_at": Decimal("940000.00"), "stock": 6},
                    {"sku": "CL-613-26", "length": 26, "color": "Platinum Blonde", "density": "200%", "price": Decimal("960000.00"), "compare_at": Decimal("1140000.00"), "stock": 4},
                ],
                "reviews": [("Sandra M.", 5, "Platinum perfection", "Zero yellow brassiness. High-fashion statement piece.")]
            },
            {
                "name": "CrownLuxe Ombre Warm Caramel to Honey Blonde Wave Wig",
                "slug": "crownluxe-ombre-warm-caramel-to-honey-blonde-wave-wig",
                "category": "colored-wigs", "subcategory": "ombre-sub",
                "hair_type": "human", "hair_origin": "malaysian",
                "texture": "Body Wave", "default_length_inches": 22,
                "default_color": "Ombre", "default_lace_type": "5x5 HD Closure",
                "description": "Seamless transition from natural dark roots to warm golden caramel and honey blonde tips.",
                "is_featured": False, "is_best_seller": False, "is_new_arrival": False,
                "collections": ["trending-now", "everyday-wigs"],
                "images": ["/images/categories/colored-highlights.jpg"],
                "variants": [
                    {"sku": "CL-OMB-18", "length": 18, "color": "Ombre", "density": "180%", "price": Decimal("580000.00"), "compare_at": Decimal("690000.00"), "stock": 8},
                    {"sku": "CL-OMB-22", "length": 22, "color": "Ombre", "density": "200%", "price": Decimal("720000.00"), "compare_at": Decimal("850000.00"), "stock": 6},
                ],
                "reviews": [("Tendo S.", 5, "Flawless ombre gradient", "No harsh horizontal lines, just a smooth natural fade.")]
            },
            {
                "name": "CrownLuxe Rich Chocolate Brown #4 Silky Straight Wig",
                "slug": "crownluxe-rich-chocolate-brown-4-silky-straight-wig",
                "category": "colored-wigs", "subcategory": "chocolate-brown-sub",
                "hair_type": "human", "hair_origin": "indian",
                "texture": "Silky Straight", "default_length_inches": 24,
                "default_color": "Chocolate Brown", "default_lace_type": "13x4 HD Frontal",
                "description": "Solid warm chocolate brown #4 with caramel glints. Flattering, soft alternative to jet black hair.",
                "is_featured": False, "is_best_seller": False, "is_new_arrival": True,
                "collections": ["new-arrivals", "work-and-office-looks", "long-hair-collection"],
                "images": ["/images/categories/colored-highlights.jpg"],
                "variants": [
                    {"sku": "CL-CHOC-20", "length": 20, "color": "Chocolate Brown", "density": "180%", "price": Decimal("620000.00"), "compare_at": Decimal("730000.00"), "stock": 9},
                    {"sku": "CL-CHOC-24", "length": 24, "color": "Chocolate Brown", "density": "200%", "price": Decimal("770000.00"), "compare_at": Decimal("910000.00"), "stock": 6},
                ],
                "reviews": [("Diana K.", 5, "Warm and elegant", "The chocolate shade softens my facial features beautifully.")]
            },

            # --- 8. SPECIALTY WIGS ---
            {
                "name": "CrownLuxe 360 Full Lace High-Ponytail Body Wave Wig",
                "slug": "crownluxe-360-full-lace-high-ponytail-body-wave-wig",
                "category": "specialty-wigs", "subcategory": "360-lace-wigs-sub",
                "hair_type": "human", "hair_origin": "brazilian",
                "texture": "Body Wave", "default_length_inches": 26,
                "default_color": "Natural Black", "default_lace_type": "360 Full Perimeter HD Lace",
                "description": "Lace wraps entirely around your hairline and nape. Allows sky-high ponytails, top knots, and braided updos.",
                "is_featured": True, "is_best_seller": False, "is_new_arrival": False,
                "collections": ["wedding-and-special-occasion", "premium-collection", "long-hair-collection"],
                "images": ["/images/categories/hd-lace-front.jpg"],
                "variants": [
                    {"sku": "CL-360-22", "length": 22, "color": "Natural Black", "density": "200%", "price": Decimal("790000.00"), "compare_at": Decimal("940000.00"), "stock": 7},
                    {"sku": "CL-360-26", "length": 26, "color": "Natural Black", "density": "250%", "price": Decimal("980000.00"), "compare_at": Decimal("1160000.00"), "stock": 5},
                ],
                "reviews": [("Peace M.", 5, "Updo queen", "Put it up in a sleek high bun and the back looked totally natural.")]
            },
            {
                "name": "CrownLuxe Headband Slip-On Deep Wave Travel Wig",
                "slug": "crownluxe-headband-slip-on-deep-wave-travel-wig",
                "category": "specialty-wigs", "subcategory": "headband-wigs-sub",
                "hair_type": "human", "hair_origin": "unspecified",
                "texture": "Deep Wave", "default_length_inches": 18,
                "default_color": "Natural Black", "default_lace_type": "No Lace (Attached Satin Headband)",
                "description": "The ultimate travel companion. Zero lace cutting or glue. Slip on, secure with velcro strap, and add your favorite decorative headband.",
                "is_featured": False, "is_best_seller": True, "is_new_arrival": False,
                "collections": ["affordable-finds", "everyday-wigs", "beginner-friendly-wigs"],
                "images": ["/images/categories/deep-wave.jpg"],
                "variants": [
                    {"sku": "CL-HB-16", "length": 16, "color": "Natural Black", "density": "150%", "price": Decimal("350000.00"), "compare_at": Decimal("430000.00"), "stock": 20},
                    {"sku": "CL-HB-20", "length": 20, "color": "Natural Black", "density": "180%", "price": Decimal("430000.00"), "compare_at": Decimal("520000.00"), "stock": 14},
                ],
                "reviews": [("Kellen N.", 5, "Great for road trips", "Keep it in my glove compartment. Whenever I need to look polished quickly, it's there.")]
            },
            {
                "name": "CrownLuxe Pixie Cut Short Tapered Textured Wig",
                "slug": "crownluxe-pixie-cut-short-tapered-textured-wig",
                "category": "specialty-wigs", "subcategory": "pixie-wigs-sub",
                "hair_type": "human", "hair_origin": "unspecified",
                "texture": "Straight Bob", "default_length_inches": 10,
                "default_color": "Jet Black", "default_lace_type": "Machine Made Stretch Cap with Tapered Nape",
                "description": "Sophisticated short cropped pixie cut with feathered crown layers and tapered neck edge. Chic statement style.",
                "is_featured": False, "is_best_seller": False, "is_new_arrival": True,
                "collections": ["short-hair-collection", "affordable-finds", "work-and-office-looks"],
                "images": ["/images/categories/bob-wigs.jpg"],
                "variants": [
                    {"sku": "CL-PIX-10", "length": 10, "color": "Jet Black", "density": "150%", "price": Decimal("320000.00"), "compare_at": Decimal("390000.00"), "stock": 12},
                ],
                "reviews": [("Christine B.", 5, "Ageless chic", "Accentuates cheekbones so well. Zero heat styling required.")]
            },
            {
                "name": "CrownLuxe French Bangs Silky Bone Straight Wig",
                "slug": "crownluxe-french-bangs-silky-bone-straight-wig",
                "category": "specialty-wigs", "subcategory": "bangs-and-fringe-wigs-sub",
                "hair_type": "human", "hair_origin": "vietnamese",
                "texture": "Bone Straight", "default_length_inches": 22,
                "default_color": "Natural Black", "default_lace_type": "Machine Made Breathable Cap with Bangs",
                "description": "Edgy, high-fashion full French fringe bangs with sleek bone straight length. No lace blending required.",
                "is_featured": False, "is_best_seller": False, "is_new_arrival": False,
                "collections": ["everyday-wigs", "long-hair-collection"],
                "images": ["/images/categories/bone-straight.jpg"],
                "variants": [
                    {"sku": "CL-BANG-20", "length": 20, "color": "Natural Black", "density": "180%", "price": Decimal("520000.00"), "compare_at": Decimal("630000.00"), "stock": 9},
                    {"sku": "CL-BANG-24", "length": 24, "color": "Natural Black", "density": "200%", "price": Decimal("670000.00"), "compare_at": Decimal("790000.00"), "stock": 7},
                ],
                "reviews": [("Olivia A.", 5, "Dramatic and sleek", "The bangs are full and cut just right.")]
            },

            # --- 9. HAIR EXTENSIONS & BUNDLES ---
            {
                "name": "CrownLuxe Raw Virgin Hair Bundles (3-Pack) + 5x5 HD Closure",
                "slug": "crownluxe-raw-virgin-hair-bundles-3pack-5x5-hd-closure",
                "category": "hair-extensions", "subcategory": "bundles-and-closures",
                "hair_type": "human", "hair_origin": "brazilian",
                "texture": "Body Wave", "default_length_inches": 24,
                "default_color": "Natural Black", "default_lace_type": "5x5 HD Swiss Closure",
                "description": "Triple machine-wefted virgin bundles (3 bundles: 20\", 22\", 24\") paired with matching 5x5 HD Swiss lace closure. Cuticle-aligned to prevent tangling.",
                "is_featured": True, "is_best_seller": True, "is_new_arrival": False,
                "collections": ["best-sellers", "premium-collection"],
                "images": ["/images/categories/hair-bundles.jpg"],
                "variants": [
                    {"sku": "CL-BDL-18", "length": 18, "color": "Natural Black", "density": "200%", "price": Decimal("580000.00"), "compare_at": Decimal("690000.00"), "stock": 14},
                    {"sku": "CL-BDL-24", "length": 24, "color": "Natural Black", "density": "200%", "price": Decimal("750000.00"), "compare_at": Decimal("890000.00"), "stock": 10},
                    {"sku": "CL-BDL-30", "length": 30, "color": "Natural Black", "density": "250%", "price": Decimal("980000.00"), "compare_at": Decimal("1160000.00"), "stock": 6},
                ],
                "reviews": [("Prossy N.", 5, "Very full bundles", "My hair stylist made a custom wig out of these and it feels so heavy and healthy.")]
            },
            {
                "name": "CrownLuxe Raw Cuticle-Aligned Bone Straight Bundles (3-Pack)",
                "slug": "crownluxe-raw-cuticle-aligned-bone-straight-bundles-3pack",
                "category": "hair-extensions", "subcategory": "bundles-and-closures",
                "hair_type": "human", "hair_origin": "peruvian",
                "texture": "Bone Straight", "default_length_inches": 26,
                "default_color": "Natural Black", "default_lace_type": "Wefted Hair Bundles",
                "description": "100% Raw unprocessed Peruvian virgin straight hair bundles. Full wefts from top to bottom that flat iron to needle-sharp sleekness.",
                "is_featured": False, "is_best_seller": False, "is_new_arrival": True,
                "collections": ["new-arrivals", "long-hair-collection"],
                "images": ["/images/categories/hair-bundles.jpg"],
                "variants": [
                    {"sku": "CL-SBDL-22", "length": 22, "color": "Natural Black", "density": "200%", "price": Decimal("680000.00"), "compare_at": Decimal("800000.00"), "stock": 8},
                    {"sku": "CL-SBDL-26", "length": 26, "color": "Natural Black", "density": "200%", "price": Decimal("840000.00"), "compare_at": Decimal("990000.00"), "stock": 7},
                ],
                "reviews": [("Gloria M.", 5, "Silk press in a bundle", "Softest bundles I've bought in Uganda. Zero shedding.")]
            },
            {
                "name": "CrownLuxe 13x4 Ear-to-Ear HD Frontal Piece (Solo)",
                "slug": "crownluxe-13x4-ear-to-ear-hd-frontal-piece-solo",
                "category": "hair-extensions", "subcategory": "frontal-pieces",
                "hair_type": "human", "hair_origin": "brazilian",
                "texture": "Body Wave", "default_length_inches": 18,
                "default_color": "Natural Black", "default_lace_type": "13x4 HD Invisible Swiss Lace Frontal",
                "description": "Replacement HD frontal piece for custom wig builds or salon sew-ins. Pre-plucked natural hairline with single micro knots.",
                "is_featured": False, "is_best_seller": False, "is_new_arrival": False,
                "collections": ["affordable-finds"],
                "images": ["/images/categories/hd-lace-front.jpg"],
                "variants": [
                    {"sku": "CL-SOLO-16", "length": 16, "color": "Natural Black", "density": "150%", "price": Decimal("310000.00"), "compare_at": Decimal("380000.00"), "stock": 15},
                    {"sku": "CL-SOLO-18", "length": 18, "color": "Natural Black", "density": "150%", "price": Decimal("360000.00"), "compare_at": Decimal("440000.00"), "stock": 10},
                ],
                "reviews": [("Stylist Becky", 5, "A stylist's dream", "The lace is so thin my clients always leave ecstatic. Easy to bleach.")]
            },
        ]

        # Populate products, variants, images, collections, reviews
        created_count = 0
        updated_count = 0
        for pdata in products_data:
            cat = cat_map[pdata["category"]]
            subcat = subcat_map.get(pdata.get("subcategory"))

            prod, created = Product.objects.update_or_create(
                slug=pdata["slug"],
                defaults={
                    "name": pdata["name"],
                    "sku": pdata["variants"][0]["sku"],
                    "category": cat,
                    "subcategory": subcat,
                    "hair_type": pdata["hair_type"],
                    "hair_origin": pdata.get("hair_origin", "unspecified"),
                    "texture": pdata["texture"],
                    "default_length_inches": pdata["default_length_inches"],
                    "default_color": pdata["default_color"],
                    "default_lace_type": pdata["default_lace_type"],
                    "description": pdata["description"],
                    "is_published": True,
                    "is_featured": pdata.get("is_featured", False),
                    "is_best_seller": pdata.get("is_best_seller", False),
                    "is_new_arrival": pdata.get("is_new_arrival", False),
                }
            )

            # Assign collections
            if "collections" in pdata:
                prod_cols = [collection_map[cslug] for cslug in pdata["collections"] if cslug in collection_map]
                prod.collections.set(prod_cols)

            if created:
                created_count += 1
            else:
                updated_count += 1

            # Seed images
            for idx, img_url in enumerate(pdata["images"]):
                ProductImage.objects.update_or_create(
                    product=prod,
                    image_url=img_url,
                    defaults={
                        "alt_text": f"{prod.name} product photography",
                        "is_primary": idx == 0,
                        "sort_order": idx
                    }
                )

            # Seed variants
            for vdata in pdata["variants"]:
                ProductVariant.objects.update_or_create(
                    sku=vdata["sku"],
                    defaults={
                        "product": prod,
                        "length_inches": vdata["length"],
                        "color": vdata["color"],
                        "texture": pdata["texture"],
                        "lace_type": pdata["default_lace_type"],
                        "density": vdata.get("density", "180%"),
                        "cap_size": "Medium 22.5\"",
                        "price": vdata["price"],
                        "compare_at_price": vdata.get("compare_at"),
                        "stock_quantity": vdata["stock"],
                        "is_active": True,
                    }
                )

            # Seed reviews
            for reviewer, rating, title, comment in pdata.get("reviews", []):
                Review.objects.get_or_create(
                    product=prod,
                    reviewer_name=reviewer,
                    title=title,
                    defaults={
                        "rating": rating,
                        "comment": comment,
                        "is_verified_purchase": True,
                        "is_approved": True
                    }
                )

        self.stdout.write(self.style.SUCCESS(
            f"Successfully seeded {created_count} created, {updated_count} updated products ({len(products_data)} total distinct wigs)!"
        ))
        self.stdout.write(self.style.SUCCESS("CrownLuxe E-Commerce Store Seeding Complete!"))
