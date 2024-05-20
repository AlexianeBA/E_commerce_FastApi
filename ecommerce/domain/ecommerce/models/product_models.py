from piccolo.table import Table
from piccolo.columns import (
    Varchar,
    Integer,
    Boolean,
    Timestamp,
    Serial,
    ForeignKey,
    Date,
)
from datetime import datetime
from enum import Enum
from domain.ecommerce.models.users_models import User


class Category(str, Enum):
    informatique = "informatique"
    telephonie = "telephonie"
    electromenager = "electromenager"
    mode = "mode"
    beaute = "beaute"
    maison = "maison"
    jardin = "jardin"
    sport = "sport"
    auto = "auto"
    moto = "moto"
    bricolage = "bricolage"
    animalerie = "animalerie"
    jouets = "jouets"
    enfant = "enfant"
    culture = "culture"
    loisirs = "loisirs"
    livres = "livres"
    musique = "musique"
    films = "films"
    instruments = "instruments"
    materiel_professionnel = "materiel_professionnel"
    services = "services"
    autres = "autres"


class Product(Table, tablename="dashboard_product"):
    id = Serial(null=False, primary_key=True)
    name = Varchar()
    price = Integer()
    stock = Integer()
    user_id = ForeignKey(User)
    category = Varchar(length=255, choices=Category, default=Category.autres.value)
    rating = Integer()
    in_stock = Boolean(default=True)
    on_sale = Boolean(default=False)
    is_new = Boolean(default=False)
    description = Varchar()
    image_url = Varchar()
    discount = Integer(default=0)
    discount_end_date = Date()
    date_created = Timestamp(default=datetime.now())
    seller_id = ForeignKey(User)

    @property
    async def username(self):
        user = await User.objects().where(User.id == self.user_id).first().run()
        return user.username if user else None
