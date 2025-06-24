# from sqlalchemy import String, text
# from sqlalchemy.orm import Mapped, mapped_column

# from config import Base


# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func
# from sqlalchemy import (
#     Column, Integer, String, Boolean, Date, DateTime, 
#     Numeric, ForeignKey, UniqueConstraint, CheckConstraint
# )


# # class User(Base):
# #     """
# #     User's model definitions
# #     """

# #     __tablename__ = "users"

# #     username: Mapped[int] = mapped_column(primary_key=True, index=True)

# #     email: Mapped[str | None] = mapped_column(String(255), unique=True, index=True)
# #     password: Mapped[bytes] = mapped_column()

# #     name: Mapped[str | None] = mapped_column(String(255))
# #     phone_number: Mapped[str | None]
# #     avatar: Mapped[str | None] = mapped_column(unique=True)
# #     about: Mapped[str | None]

# #     is_staff: Mapped[bool] = mapped_column(default=False, server_default=text("FALSE"))
# #     is_active: Mapped[bool] = mapped_column(default=True, server_default=text("TRUE"))
# #     is_superuser: Mapped[bool] = mapped_column(
# #         default=False, server_default=text("FALSE")
# #     )


# class StockExchange(Base):
#     __tablename__ = "stock_exchanges"

#     exchange_id: Mapped[int] = mapped_column(primary_key=True)
#     exchange_code: Mapped[str] = mapped_column(unique=True, nullable=False)
#     name: Mapped[str] = mapped_column(String(100), nullable=False)
#     country: Mapped[str] = mapped_column(String(50), nullable=False)
#     established_date: Mapped[Date] = mapped_column(Date)
#     is_active: Mapped[bool] = mapped_column(Boolean, default=True)
#     website_url: Mapped[str] = mapped_column(String(255))
#     created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

#     # One-to-one relationship with ExchangeDetails
#     details:Mapped['ExchangeDetails'] = relationship(back_populates="exchange", uselist=False)

#     # One-to-many relationship with Stocks
#     stocks:Mapped["Stock"] = relationship(
#          back_populates="exchange", cascade="all, delete-orphan"
#     )


# class ExchangeDetails(Base):
#     __tablename__ = "exchange_details"

#     detail_id: Mapped[] = mapped_column(Integer, primary_key=True)
#     exchange_id: Mapped[] = mapped_column(
#         Integer,
#         ForeignKey("stock_exchanges.exchange_id", ondelete="CASCADE"),
#         unique=True,
#         nullable=False,
#     )
#     timezone: Mapped[] = mapped_column(String(50), nullable=False)
#     trading_hours: Mapped[] = mapped_column(String(100))
#     market_cap_usd: Mapped[] = mapped_column(Numeric(20, 2))
#     listed_companies: Mapped[] = mapped_column(Integer)
#     settlement_period_days: Mapped[] = mapped_column(Integer, default=2)
#     last_updated: Mapped[] = mapped_column(
#         DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
#     )

#     # One-to-one relationship back to StockExchange
#     exchange = relationship("StockExchange", back_populates="details")


# class Stock(Base):
#     __tablename__ = "stocks"

#     stock_id: Mapped[] = mapped_column(Integer, primary_key=True)
#     exchange_id: Mapped[] = mapped_column(
#         Integer,
#         ForeignKey("stock_exchanges.exchange_id", ondelete="CASCADE"),
#         nullable=False,
#     )
#     ticker_symbol: Mapped[] = mapped_column(String(10), nullable=False)
#     company_name: Mapped[] = mapped_column(String(100), nullable=False)
#     sector: Mapped[] = mapped_column(String(50))
#     industry: Mapped[] = mapped_column(String(50))
#     listing_date: Mapped[] = mapped_column(Date)
#     is_active: Mapped[] = mapped_column(Boolean, default=True)
#     ipo_price: Mapped[] = mapped_column(Numeric(10, 2))
#     current_price: Mapped[] = mapped_column(Numeric(10, 2))
#     market_cap: Mapped[] = mapped_column(Numeric(20, 2))
#     dividend_yield: Mapped[] = mapped_column(Numeric(5, 2))

#     # Many-to-one relationship with StockExchange
#     exchange = relationship("StockExchange", back_populates="stocks")

#     # One-to-many relationship with StockPriceHistory
#     price_history = relationship(
#         "StockPriceHistory", back_populates="stock", cascade="all, delete-orphan"
#     )

#     # Many-to-many relationship with Currency through StockCurrencyPair
#     currency_pairs = relationship(
#         "StockCurrencyPair", back_populates="stock", cascade="all, delete-orphan"
#     )

#     __table_args__ = (
#         UniqueConstraint(
#             "exchange_id", "ticker_symbol", name="unique_stock_per_exchange"
#         ),
#     )


# class Currency(Base):
#     __tablename__ = "currencies"

#     currency_id: Mapped[] = mapped_column(Integer, primary_key=True)
#     currency_code: Mapped[] = mapped_column(String(3), unique=True, nullable=False)
#     currency_name: Mapped[] = mapped_column(String(50), nullable=False)
#     country: Mapped[] = mapped_column(String(50))
#     is_crypto: Mapped[] = mapped_column(Boolean, default=False)
#     created_at: Mapped[] = mapped_column(DateTime(timezone=True), server_default=func.now())

#     # Relationships for base and quote currencies
#     base_pairs = relationship(
#         "StockCurrencyPair",
#         foreign_keys="[StockCurrencyPair.base_currency_id]",
#         back_populates="base_currency",
#     )
#     quote_pairs = relationship(
#         "StockCurrencyPair",
#         foreign_keys="[StockCurrencyPair.quote_currency_id]",
#         back_populates="quote_currency",
#     )


# class StockCurrencyPair(Base):
#     __tablename__ = "stock_currency_pairs"

#     pair_id: Mapped[] = mapped_column(Integer, primary_key=True)
#     stock_id: Mapped[] = mapped_column(
#         Integer, ForeignKey("stocks.stock_id", ondelete="CASCADE"), nullable=False
#     )
#     base_currency_id: Mapped[] = mapped_column(
#         Integer,
#         ForeignKey("currencies.currency_id", ondelete="CASCADE"),
#         nullable=False,
#     )
#     quote_currency_id: Mapped[] = mapped_column(
#         Integer,
#         ForeignKey("currencies.currency_id", ondelete="CASCADE"),
#         nullable=False,
#     )
#     is_primary_pair: Mapped[] = mapped_column(Boolean, default=False)
#     last_traded_price: Mapped[] = mapped_column(Numeric(20, 6))
#     daily_volume: Mapped[] = mapped_column(Numeric(20, 2))
#     created_at: Mapped[] = mapped_column(DateTime(timezone=True), server_default=func.now())

#     # Many-to-one relationships
#     stock = relationship("Stock", back_populates="currency_pairs")
#     base_currency = relationship(
#         "Currency", foreign_keys=[base_currency_id], back_populates="base_pairs"
#     )
#     quote_currency = relationship(
#         "Currency", foreign_keys=[quote_currency_id], back_populates="quote_pairs"
#     )

#     # One-to-many relationship with StockPriceHistory
#     price_history = relationship("StockPriceHistory", back_populates="currency_pair")

#     __table_args__ = (
#         UniqueConstraint(
#             "stock_id",
#             "base_currency_id",
#             "quote_currency_id",
#             name="unique_currency_pair",
#         ),
#         CheckConstraint(
#             "base_currency_id != quote_currency_id", name="different_currencies"
#         ),
#     )


# class StockPriceHistory(Base):
#     __tablename__ = "stock_price_history"

#     price_id: Mapped[] = mapped_column(Integer, primary_key=True)
#     stock_id: Mapped[] = mapped_column(
#         Integer, ForeignKey("stocks.stock_id", ondelete="CASCADE"), nullable=False
#     )
#     currency_pair_id: Mapped[] = mapped_column(
#         Integer, ForeignKey("stock_currency_pairs.pair_id", ondelete="SET NULL")
#     )
#     price_date: Mapped[] = mapped_column(DateTime(timezone=True), nullable=False)
#     open_price: Mapped[] = mapped_column(Numeric(10, 2))
#     high_price: Mapped[] = mapped_column(Numeric(10, 2))
#     low_price: Mapped[] = mapped_column(Numeric(10, 2))
#     close_price: Mapped[] = mapped_column(Numeric(10, 2))
#     adjusted_close: Mapped[] = mapped_column(Numeric(10, 2))
#     volume: Mapped[] = mapped_column(BigInteger)
#     created_at: Mapped[] = mapped_column(DateTime(timezone=True), server_default=func.now())

#     # Many-to-one relationships
#     stock = relationship("Stock", back_populates="price_history")
#     currency_pair = relationship("StockCurrencyPair", back_populates="price_history")
