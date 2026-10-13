from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from catalog.models import Category, Product, ProductVariant, ProductImage, Review
from orders.models import DeliveryMethod
from promotions.models import Coupon
from users.models import Profile, Address

User = get_user_model()

class Command(BaseCommand):
    help = "Seeds database with CrownLuxe categories, products, variants, images, delivery zones, and coupons."

    def handle(self, *args, **options):
        self.stdout.write("Seeding CrownLuxe E-Commerce Store...")

        # 1. Superuser / Admin
        admin_user, created = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@crownluxe.com", "first_name": "Store", "last_name": "Admin", "is_staff": True, "is_superuser": True}
        )
        if created:
            admin_user.set_password("admin123456")
            admin_user.save()
            Profile.objects.get_or_create(user=admin_user, phone="+256700112233")
            self.stdout.write(self.style.SUCCESS("Created admin user (admin / admin123456)"))

        # Demo customer
        customer_user, created = User.objects.get_or_create(
            username="nakato_e",
            defaults={"email": "nakato@example.com", "first_name": "Eva", "last_name": "Nakato"}
        )
        if created:
            customer_user.set_password("customer123")
            customer_user.save()
            Profile.objects.get_or_create(user=customer_user, phone="+256772987654")
            Address.objects.create(
                user=customer_user,
                full_name="Eva Nakato",
                phone="+256772987654",
                street_address="Plot 14 Acacia Avenue, Kololo",
                city_or_zone="Kampala Central",
                country="Uganda",
                is_default=True
            )
            self.stdout.write(self.style.SUCCESS("Created demo customer (nakato_e / customer123)"))

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
        self.stdout.write(self.style.SUCCESS("Seeded delivery methods."))

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
        self.stdout.write(self.style.SUCCESS("Seeded promotional coupons."))

        # 4. Categories
        categories_data = [
            ("Human Hair Wigs", "100% Virgin unprocessed human hair wigs with natural hairline.", "https://images.unsplash.com/photo-1595476108010-b4d1f102b1b1?auto=format&fit=crop&w=600&q=80", 1),
            ("HD Lace Front Wigs", "Ultra-thin melted invisible HD swiss lace for imperceptible blend.", "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=600&q=80", 2),
            ("Glueless & Wear-Go Wigs", "Pre-cut lace, pre-plucked, zero adhesive needed in 30 seconds.", "https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=600&q=80", 3),
            ("Bone Straight Wigs", "Silky, mirror-shine bone straight human hair that stays sleek.", "https://images.unsplash.com/photo-1580618672591-eb180b1a973f?auto=format&fit=crop&w=600&q=80", 4),
            ("Deep Wave & Curly Wigs", "Lush bouncy defined curls with high volume and luscious texture.", "https://images.unsplash.com/photo-1519699047748-de8e457a634e?auto=format&fit=crop&w=600&q=80", 5),
            ("Bob Wigs", "Chic blunt cut, asymmetrical, and timeless bob styles for everyday glam.", "https://images.unsplash.com/photo-1582095133179-bfd08e2fc6b3?auto=format&fit=crop&w=600&q=80", 6),
            ("Colored & Highlight Wigs", "Trendy piano highlights, 613 platinum blonde, and 99J burgundy.", "https://images.unsplash.com/photo-1562004760-aceed7bb0fe3?auto=format&fit=crop&w=600&q=80", 7),
            ("Hair Extensions & Bundles", "Raw donor virgin hair bundles, closures, and frontals.", "https://images.unsplash.com/photo-1516914943479-89db7d9ae7f2?auto=format&fit=crop&w=600&q=80", 8),
        ]
        cat_map = {}
        for name, desc, img, order in categories_data:
            cat, _ = Category.objects.update_or_create(
                name=name,
                defaults={"description": desc, "image_url": img, "sort_order": order, "is_active": True}
            )
            cat_map[name] = cat
        self.stdout.write(self.style.SUCCESS("Seeded categories."))

        # 5. Products & Variants & Reviews
        products_data = [
            {
                "name": "CrownLuxe 13x4 HD Lace Bone Straight Human Hair Wig",
                "category": "Bone Straight Wigs",
                "hair_type": "human",
                "texture": "Bone Straight",
                "default_length_inches": 24,
                "default_color": "1B Natural Black",
                "default_lace_type": "13x4 HD Invisible Lace",
                "description": "Our signature luxury virgin human hair wig. Featuring ultra-thin transparent HD lace that melts seamlessly into all skin tones. 100% Brazilian virgin hair that flat irons to needle-sleek bone straight with intense natural luster.",
                "is_featured": True,
                "is_best_seller": True,
                "is_new_arrival": False,
                "images": [
                    ("https://images.unsplash.com/photo-1580618672591-eb180b1a973f?auto=format&fit=crop&w=1000&q=85", "CrownLuxe Bone Straight Wig Front View", True),
                    ("https://images.unsplash.com/photo-1595476108010-b4d1f102b1b1?auto=format&fit=crop&w=1000&q=85", "CrownLuxe Bone Straight Hairline Detail", False),
                    ("https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=1000&q=85", "CrownLuxe Bone Straight Styled Model", False),
                ],
                "variants": [
                    {"sku": "CL-BS-18", "length": 18, "color": "1B Natural Black", "lace": "13x4 HD Lace", "price": Decimal("480000.00"), "compare_at": Decimal("580000.00"), "stock": 12},
                    {"sku": "CL-BS-22", "length": 22, "color": "1B Natural Black", "lace": "13x4 HD Lace", "price": Decimal("620000.00"), "compare_at": Decimal("750000.00"), "stock": 18},
                    {"sku": "CL-BS-26", "length": 26, "color": "1B Natural Black", "lace": "13x4 HD Lace", "price": Decimal("790000.00"), "compare_at": Decimal("920000.00"), "stock": 9},
                    {"sku": "CL-BS-30", "length": 30, "color": "1B Natural Black", "lace": "13x4 HD Lace", "price": Decimal("950000.00"), "compare_at": Decimal("1100000.00"), "stock": 5},
                ],
                "reviews": [
                    ("Sarah K.", 5, "Unbelievable quality!", "The lace literally vanished into my skin! Best straight wig in Kampala hands down. Doesn't tangle at all."),
                    ("Brenda A.", 5, "Pure luxury", "So soft and silky. Delivered to my office in Kololo within 2 hours!"),
                ]
            },
            {
                "name": "Luxe Deep Wave 13x6 Melted Frontal Wig",
                "category": "Deep Wave & Curly Wigs",
                "hair_type": "human",
                "texture": "Deep Wave",
                "default_length_inches": 26,
                "default_color": "1B Natural Black",
                "default_lace_type": "13x6 HD Ear-to-Ear Lace",
                "description": "Exquisite deep wave curls designed for maximum bounce and fullness. Pre-plucked natural hairline with delicate baby hairs. Wet and wavy versatility that holds definition all day.",
                "is_featured": True,
                "is_best_seller": True,
                "is_new_arrival": False,
                "images": [
                    ("https://images.unsplash.com/photo-1519699047748-de8e457a634e?auto=format&fit=crop&w=1000&q=85", "Deep Wave Curly Frontal Wig", True),
                    ("https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=1000&q=85", "Deep Wave Texture Close-up", False),
                ],
                "variants": [
                    {"sku": "CL-DW-20", "length": 20, "color": "1B Natural Black", "lace": "13x6 HD Lace", "price": Decimal("540000.00"), "compare_at": Decimal("650000.00"), "stock": 14},
                    {"sku": "CL-DW-24", "length": 24, "color": "1B Natural Black", "lace": "13x6 HD Lace", "price": Decimal("680000.00"), "compare_at": Decimal("800000.00"), "stock": 10},
                    {"sku": "CL-DW-28", "length": 28, "color": "1B Natural Black", "lace": "13x6 HD Lace", "price": Decimal("850000.00"), "compare_at": Decimal("990000.00"), "stock": 6},
                ],
                "reviews": [
                    ("Grace T.", 5, "The curls are breathtaking", "Water and mousse are all you need. Wore it to a wedding and got non-stop compliments."),
                ]
            },
            {
                "name": "Glueless Pre-Cut 4x4 Wear & Go Blunt Bob Wig",
                "category": "Bob Wigs",
                "hair_type": "human",
                "texture": "Straight Bob",
                "default_length_inches": 12,
                "default_color": "Natural Black",
                "default_lace_type": "Pre-Cut Glueless 4x4",
                "description": "Zero skills required. Put on and go in 30 seconds with our pre-cut invisible lace and upgraded elastic grip band. Sharp blunt cut ends that hug your jawline perfectly.",
                "is_featured": True,
                "is_best_seller": False,
                "is_new_arrival": True,
                "images": [
                    ("https://images.unsplash.com/photo-1582095133179-bfd08e2fc6b3?auto=format&fit=crop&w=1000&q=85", "Glueless Blunt Cut Bob Wig", True),
                    ("https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=1000&q=85", "Bob Wig Profile Angle", False),
                ],
                "variants": [
                    {"sku": "CL-BOB-10", "length": 10, "color": "Natural Black", "lace": "Pre-cut 4x4", "price": Decimal("280000.00"), "compare_at": Decimal("350000.00"), "stock": 20},
                    {"sku": "CL-BOB-12", "length": 12, "color": "Natural Black", "lace": "Pre-cut 4x4", "price": Decimal("320000.00"), "compare_at": Decimal("390000.00"), "stock": 16},
                    {"sku": "CL-BOB-14", "length": 14, "color": "Natural Black", "lace": "Pre-cut 4x4", "price": Decimal("360000.00"), "compare_at": Decimal("440000.00"), "stock": 8},
                ],
                "reviews": [
                    ("Patricia M.", 5, "Game changer for busy mornings", "Literally slip it on and walk out the door. The lace is already cut and looks so natural."),
                ]
            },
            {
                "name": "Honey Blonde Piano Highlight P4/27 Body Wave Wig",
                "category": "Colored & Highlight Wigs",
                "hair_type": "human",
                "texture": "Body Wave",
                "default_length_inches": 24,
                "default_color": "P4/27 Honey Blonde Piano",
                "default_lace_type": "13x4 Transparent Lace",
                "description": "Stunning caramel and honey blonde streaks expertly blended into rich warm brown undertones. Silky body wave body that moves with effortless drama.",
                "is_featured": True,
                "is_best_seller": True,
                "is_new_arrival": False,
                "images": [
                    ("https://images.unsplash.com/photo-1562004760-aceed7bb0fe3?auto=format&fit=crop&w=1000&q=85", "Piano Highlight Honey Blonde Wig", True),
                    ("https://images.unsplash.com/photo-1519699047748-de8e457a634e?auto=format&fit=crop&w=1000&q=85", "Highlights Body Wave View", False),
                ],
                "variants": [
                    {"sku": "CL-HL-20", "length": 20, "color": "P4/27 Piano Highlight", "lace": "13x4 Lace", "price": Decimal("590000.00"), "compare_at": Decimal("720000.00"), "stock": 7},
                    {"sku": "CL-HL-24", "length": 24, "color": "P4/27 Piano Highlight", "lace": "13x4 Lace", "price": Decimal("720000.00"), "compare_at": Decimal("860000.00"), "stock": 11},
                    {"sku": "CL-HL-28", "length": 28, "color": "P4/27 Piano Highlight", "lace": "13x4 Lace", "price": Decimal("890000.00"), "compare_at": Decimal("1050000.00"), "stock": 4},
                ],
                "reviews": [
                    ("Daphne N.", 5, "The color is so rich!", "Color is identical to pictures. No shedding even after washing. 10/10 recommended!"),
                ]
            },
            {
                "name": "Platinum Ice 613 Blonde 13x4 Transparent Frontal Wig",
                "category": "Colored & Highlight Wigs",
                "hair_type": "human",
                "texture": "Straight",
                "default_length_inches": 26,
                "default_color": "613 Platinum Blonde",
                "default_lace_type": "13x4 Transparent Swiss Lace",
                "description": "Ready to dye or rock pure platinum. Sourced from high-grade 10A donor hair with thick full ends from root to tip. Can be colored pink, ginger, or pastel tones effortlessly.",
                "is_featured": False,
                "is_best_seller": False,
                "is_new_arrival": True,
                "images": [
                    ("https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=1000&q=85", "613 Blonde Platinum Wig", True),
                ],
                "variants": [
                    {"sku": "CL-613-22", "length": 22, "color": "613 Platinum Blonde", "lace": "13x4 Lace", "price": Decimal("680000.00"), "compare_at": Decimal("800000.00"), "stock": 6},
                    {"sku": "CL-613-26", "length": 26, "color": "613 Platinum Blonde", "lace": "13x4 Lace", "price": Decimal("820000.00"), "compare_at": Decimal("980000.00"), "stock": 5},
                    {"sku": "CL-613-30", "length": 30, "color": "613 Platinum Blonde", "lace": "13x4 Lace", "price": Decimal("990000.00"), "compare_at": Decimal("1180000.00"), "stock": 3},
                ],
                "reviews": [
                    ("Joy K.", 5, "Took color like a dream!", "Dyed it emerald green and it stayed soft and lustrous."),
                ]
            },
            {
                "name": "Bordeaux Wine Red 99J Body Wave Glueless Wig",
                "category": "Colored & Highlight Wigs",
                "hair_type": "human",
                "texture": "Body Wave",
                "default_length_inches": 22,
                "default_color": "99J Burgundy Wine",
                "default_lace_type": "13x4 HD Lace Front",
                "description": "Deep burgundy jewel tones that look regal in sunlight. Full 180% density offering unmatched volume and graceful movement.",
                "is_featured": True,
                "is_best_seller": False,
                "is_new_arrival": True,
                "images": [
                    ("https://images.unsplash.com/photo-1595476108010-b4d1f102b1b1?auto=format&fit=crop&w=1000&q=85", "99J Burgundy Body Wave Wig", True),
                ],
                "variants": [
                    {"sku": "CL-99J-20", "length": 20, "color": "99J Burgundy", "lace": "13x4 HD Lace", "price": Decimal("570000.00"), "compare_at": Decimal("690000.00"), "stock": 9},
                    {"sku": "CL-99J-24", "length": 24, "color": "99J Burgundy", "lace": "13x4 HD Lace", "price": Decimal("710000.00"), "compare_at": Decimal("850000.00"), "stock": 8},
                ],
                "reviews": [
                    ("Fiona A.", 5, "Sophisticated autumn shade", "The burgundy is deep and classy, not bright red. Exactly what I wanted."),
                ]
            },
            {
                "name": "Raw Virgin Brazilian Body Wave 5x5 HD Closure Wig",
                "category": "Human Hair Wigs",
                "hair_type": "human",
                "texture": "Body Wave",
                "default_length_inches": 22,
                "default_color": "1B Natural Black",
                "default_lace_type": "5x5 HD Lace Closure",
                "description": "Low maintenance luxury. 5x5 closure allows versatile middle or side parting with half the maintenance of a full frontal. Thick density and silky soft feel.",
                "is_featured": False,
                "is_best_seller": True,
                "is_new_arrival": False,
                "images": [
                    ("https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=1000&q=85", "5x5 HD Closure Body Wave Wig", True),
                ],
                "variants": [
                    {"sku": "CL-BW-18", "length": 18, "color": "1B Natural Black", "lace": "5x5 HD Closure", "price": Decimal("460000.00"), "compare_at": Decimal("550000.00"), "stock": 15},
                    {"sku": "CL-BW-22", "length": 22, "color": "1B Natural Black", "lace": "5x5 HD Closure", "price": Decimal("590000.00"), "compare_at": Decimal("710000.00"), "stock": 11},
                    {"sku": "CL-BW-26", "length": 26, "color": "1B Natural Black", "lace": "5x5 HD Closure", "price": Decimal("750000.00"), "compare_at": Decimal("890000.00"), "stock": 8},
                ],
                "reviews": [
                    ("Sharon B.", 5, "My everyday go-to wig", "Holds curls for 4 days straight without re-curling."),
                ]
            },
            {
                "name": "Afro Kinky Curly 13x4 Glueless Lace Wig",
                "category": "Deep Wave & Curly Wigs",
                "hair_type": "human",
                "texture": "Kinky Curly",
                "default_length_inches": 20,
                "default_color": "1B Natural Black",
                "default_lace_type": "13x4 HD Lace",
                "description": "Celebrates natural type 3C-4A curl patterns with juicy, hydrated definition. Super realistic texture that blends seamlessly with natural edges.",
                "is_featured": True,
                "is_best_seller": False,
                "is_new_arrival": False,
                "images": [
                    ("https://images.unsplash.com/photo-1519699047748-de8e457a634e?auto=format&fit=crop&w=1000&q=85", "Kinky Curly Natural Wig", True),
                ],
                "variants": [
                    {"sku": "CL-KC-18", "length": 18, "color": "1B Natural Black", "lace": "13x4 HD Lace", "price": Decimal("490000.00"), "compare_at": Decimal("600000.00"), "stock": 10},
                    {"sku": "CL-KC-22", "length": 22, "color": "1B Natural Black", "lace": "13x4 HD Lace", "price": Decimal("630000.00"), "compare_at": Decimal("770000.00"), "stock": 9},
                ],
                "reviews": [
                    ("Naomi O.", 5, "Looks like my own hair grown out!", "The texture match is unreal. Super full 200% density."),
                ]
            },
            {
                "name": "Full Lace Hand-Tied Luxury Human Hair Wig",
                "category": "HD Lace Front Wigs",
                "hair_type": "human",
                "texture": "Silky Straight",
                "default_length_inches": 28,
                "default_color": "1B Natural Black",
                "default_lace_type": "360 Full Lace Breathable Cap",
                "description": "The pinnacle of hair artistry. 100% hand-tied individual strands throughout the entire cap allowing high ponytails, updos, braids, and free-parting anywhere.",
                "is_featured": True,
                "is_best_seller": False,
                "is_new_arrival": True,
                "images": [
                    ("https://images.unsplash.com/photo-1580618672591-eb180b1a973f?auto=format&fit=crop&w=1000&q=85", "Full Lace 360 Hand Tied Wig", True),
                ],
                "variants": [
                    {"sku": "CL-FL-24", "length": 24, "color": "1B Natural Black", "lace": "Full Lace", "price": Decimal("880000.00"), "compare_at": Decimal("1050000.00"), "stock": 4},
                    {"sku": "CL-FL-28", "length": 28, "color": "1B Natural Black", "lace": "Full Lace", "price": Decimal("1100000.00"), "compare_at": Decimal("1300000.00"), "stock": 3},
                ],
                "reviews": [
                    ("Victoria N.", 5, "Worth every single shilling", "Put it in a high sleek ponytail immediately. You cannot see any tracks."),
                ]
            },
            {
                "name": "Raw Virgin Hair 3-Bundle Deal with HD Frontal",
                "category": "Hair Extensions & Bundles",
                "hair_type": "human",
                "texture": "Body Wave",
                "default_length_inches": 22,
                "default_color": "Natural Black",
                "default_lace_type": "13x4 HD Frontal",
                "description": "Bundle package deal: 3 raw donor virgin hair bundles (20\", 22\", 24\") plus a matching 13x4 HD frontal. Thick cuticles intact for multi-year reuse.",
                "is_featured": False,
                "is_best_seller": True,
                "is_new_arrival": False,
                "images": [
                    ("https://images.unsplash.com/photo-1516914943479-89db7d9ae7f2?auto=format&fit=crop&w=1000&q=85", "Virgin Bundles Deal", True),
                ],
                "variants": [
                    {"sku": "CL-BDL-182022", "length": 22, "color": "Natural Black", "lace": "13x4 Frontal", "price": Decimal("520000.00"), "compare_at": Decimal("640000.00"), "stock": 14},
                    {"sku": "CL-BDL-222426", "length": 26, "color": "Natural Black", "lace": "13x4 Frontal", "price": Decimal("680000.00"), "compare_at": Decimal("820000.00"), "stock": 10},
                ],
                "reviews": [
                    ("Agnes S.", 5, "Best bundles in town", "Wefts are double stitched, zero shedding even after washing 5 times."),
                ]
            }
        ]

        for p_data in products_data:
            cat = cat_map.get(p_data["category"])
            product, _ = Product.objects.update_or_create(
                name=p_data["name"],
                defaults={
                    "category": cat,
                    "hair_type": p_data["hair_type"],
                    "texture": p_data["texture"],
                    "default_length_inches": p_data["default_length_inches"],
                    "default_color": p_data["default_color"],
                    "default_lace_type": p_data["default_lace_type"],
                    "description": p_data["description"],
                    "is_published": True,
                    "is_featured": p_data["is_featured"],
                    "is_best_seller": p_data["is_best_seller"],
                    "is_new_arrival": p_data["is_new_arrival"],
                }
            )

            # Images
            for idx, (img_url, alt, is_prim) in enumerate(p_data["images"]):
                ProductImage.objects.update_or_create(
                    product=product,
                    image_url=img_url,
                    defaults={"alt_text": alt, "is_primary": is_prim, "sort_order": idx}
                )

            # Variants
            for v_data in p_data["variants"]:
                ProductVariant.objects.update_or_create(
                    sku=v_data["sku"],
                    defaults={
                        "product": product,
                        "length_inches": v_data["length"],
                        "color": v_data["color"],
                        "texture": p_data["texture"],
                        "lace_type": v_data["lace"],
                        "density": "180%",
                        "cap_size": "Medium (22.5\")",
                        "price": v_data["price"],
                        "compare_at_price": v_data["compare_at"],
                        "stock_quantity": v_data["stock"],
                        "is_active": True,
                    }
                )

            # Reviews
            for r_name, r_rating, r_title, r_comment in p_data["reviews"]:
                Review.objects.get_or_create(
                    product=product,
                    reviewer_name=r_name,
                    defaults={
                        "rating": r_rating,
                        "title": r_title,
                        "comment": r_comment,
                        "is_verified_purchase": True,
                        "is_approved": True,
                    }
                )

        self.stdout.write(self.style.SUCCESS("Seeded 10+ premium wig products with variants, images, and reviews!"))
        self.stdout.write(self.style.SUCCESS("CrownLuxe E-Commerce Store Seeding Complete!"))
