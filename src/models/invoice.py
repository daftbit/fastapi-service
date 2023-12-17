

import enum

class InvoiceType(enum.Enum):
    ESTIMATE = "estimate"
    SALE = "sale"


class InvoiceStatus(enum.Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    BILLED = "billed"
    PAID = "paid"
    
    