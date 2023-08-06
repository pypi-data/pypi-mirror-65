class NewLineRequest():
    """
    Since GET /order-item/:id response and the POST /order-item request don't
    match except for a few attributes, this class aims to build an OrderItem instance
    mapping these few matching attributes.
    The specification doesn't explicitly state the optimistic equivalence presented here,
    so this mapping needs to be reviewed later on.
    """

    def __init__(self, new_order_item):
        self.lineInfo = new_order_item['lineInfo'][0]

    def to_order_item(self):
        """
        Maps the atttributes of a NewLineRequest instance, as specified in Swagger,
        to the attributes of an OrderItem instance, as specified in a
        GET response.

        :return: dict
        """

        return {
            'name': self.lineInfo['name'],
            'surname': self.lineInfo['surname'],
            'phone': self.lineInfo['phoneNumber'],
            'attributes': {
                'Fecha_Portabilidad_Saliente': self.lineInfo['portabilityDate'],
                'ICCID_Donante': self.lineInfo['iccid_donante'],
                'Tipo_de_Documento': self.lineInfo['documentType'],
            },
            'simAttributes': {
                'ICCID': self.lineInfo['iccid'],
            }
        }
