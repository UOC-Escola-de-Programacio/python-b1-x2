# Write your imports here
from bills import *


class OrderType:
    # Do not change this enum
    ASC = 0
    DES = 1


class Statistics:
    def __init__(self, bills: list[Bill]):
        # Do not change this method
        self.bills = bills

    def find_top_sell_product(self) -> (Product, int):
        products = []
        productQuantities = []
        topIndex = 0

        '''
        Este bucle se encarga de revistar todas las facturas para ver
        que productos se han vendido y en que cantidades, una vez lo sabe
        los registra en una variable que usará despues para comparar.
        '''

        # Tenemos un monton de facturas, revisemoslas una por una.
        for bill in self.bills:
            # Cada factura abarca varios productos, revisemoslos uno por uno.
            for product in bill.products:
                # Tenemos este producto registrado?
                if product not in products:
                    # No, registremoslo.
                    products.append(product)
                    productQuantities.append(1)
                else:
                    # No, añadamos esta venta al registro.
                    productQuantities[products.index(product)] += 1

        '''
        Una vez sabemos que cantidades de cada producto se han vendido, las comparamos
        una por una para ver cual ha vendido más.
        '''

        # Vale, tenemos los productos y sus ventas, comparemoslos para ver cual a vendido más.
        for i in range(len(productQuantities)):
            # Ha vendido más que el actual top uno?
            if productQuantities[i] > productQuantities[topIndex]:
                # Si, pongamoslo en el top uno.
                topIndex = i

        # Vale, ya se que producto es top uno, se lo diré al jefe.
        return products[topIndex], productQuantities[topIndex]

    def find_top_two_sellers(self) -> list:
        sellers = []
        sellerImports = []
        topTwo = []
    
        '''
        Este bucle se encarga de registrar las ventas totales de los vendedores.
        Para ello toma las facturas e identifica al vendedor, una vez sabe
        quien es, añade la compra a su registro, o le crea uno propio en caso de
        no tenerlo.
        '''

        # Tenemos un monton de facturas, revisemoslas una por una.
        for bill in self.bills:
            # Tenemos a este vendedor registrado?
            if bill.seller not in sellers:
                # No, registremoslo.
                sellers.append(bill.seller)
                sellerImports.append(bill.calculate_total())
            else:
                # Si, añadamos esta compra a registro.
                sellerImports[sellers.index(bill.seller)] += bill.calculate_total()

        '''
        Una vez tenemos las ventas totales, este bucle se encarga de compararlas una por una,
        al terminar se queda con los dos con más ventas.
        '''

        # Okey, tengo los vendedores y sus ventas totales, veamos cuales son los dos que más han vendido.
        for i in range(len(sellerImports)):
            # Cuantos tengo registrados?
            if len(topTwo) == 2:
                # Dos, vale, pues toca comparalos.
                # Ha vendido más que uno de los dos?
                if sellerImports[i] > sellerImports[sellers.index(topTwo[0])]:
                    # Ha vendido más que el primero, pongamos a este de primero.
                    topTwo[1] = topTwo[0]
                    topTwo[0] = sellers[i]
                elif sellerImports[i] > sellerImports[sellers.index(topTwo[1])]:
                    # Ha vendido más que el segundo, pongamos a este de segundo.
                    topTwo[1] = sellers[i]
            elif len(topTwo) == 1:
                # Uno, comparemoslo con este unico registro.
                # Tiene más o menos?
                if sellerImports[sellers.index(topTwo[0])] > sellerImports[i]:
                    # Parece que tiene menos, pongamoslo de segundo.
                    topTwo.append(sellers[i])
                elif sellerImports[sellers.index(topTwo[0])] < sellerImports[i]:
                    # Tiene más, pongamoslo de primero.
                    topTwo.append(topTwo[0])
                    topTwo[0] = sellers[i]
            elif len(topTwo) == 0:
                # Ninguno, vale, este será el primero.
                topTwo.append(sellers[i])

        # Ya sabemos cuales el top dos de vendedores, se lo paso al jefe.
        return topTwo

    
    def find_buyer_lowest_total_purchases(self) -> (Buyer, float):
        buyers = []
        buyersTotal = []
        lesserIndex = 0
    
        '''
        Este bucle se encarga de registrar las compras totales de los clientes.
        Para ello toma las facturas e identifica al comprador, una vez sabe
        quien es, añade la compra a su registro, o le crea uno propio en caso de
        no tenerlo.
        '''

        # Tenemos un monton de facturas, revisemoslas una por una.
        for bill in self.bills:
            # Tenemos a este comprador registrado?
            if bill.buyer not in buyers:
                # No, registremoslo.
                buyers.append(bill.buyer)
                buyersTotal.append(bill.calculate_total())
            else:
                # Si, añadamos esta compra a registro.
                buyersTotal[buyers.index(bill.buyer)] += bill.calculate_total()

    
        '''
        Una vez tenemos las compras totales, este bucle se encarga de compararlas una por una,
        al terminar se queda con la más baja y la envia.
        '''

        # Okey, tengo los clientes y sus compras totales, veamos cual es el que menos ha gastado.
        for i in range(len(buyersTotal)):
            # Este ha gastado menos?
            if buyersTotal[i] < buyersTotal[lesserIndex]:
                # Si, marquemoslo.
                lesserIndex = i

        # Ya sabemos que cliente ha comprado menos, se lo paso al jefe.
        return buyers[lesserIndex], buyersTotal[lesserIndex]

    def order_products_by_tax(self, order_type: OrderType) -> tuple:
        products = []
        orderedProducts = []

        '''
        Este bucle sirve para meter todas las facturas en una lista, cuyo formato
        es: [producto, tasa]
        '''

        # Tenemos un monton de facturas, revisemoslas una por una.
        for bill in self.bills:
            # Cada factura abarca varios productos, revisemoslos uno por uno.
            for product in bill.products:
                # Parece que cada producto tiene varios impuestos, calculemoslos por separado
                # y luego juntemoslo todo.
                totalTax = 0
                for tax in product.taxes:
                    totalTax += product.calculate_tax(tax)
                # Cuantos productos tenemos registrados?
                if len(products) == 0:
                    # Ninguno, pongamos el primero.
                    products.append([product, totalTax])
                else:
                    # Ya tenemos algunos.
                    for i in range(len(products)):
                        # Este comparte id con algun otro registro?
                        if product.product_id == products[i][0].product_id:
                            # Si, añadamos el impuesto a su registro.
                            products[i][1] += totalTax
                            break
                        if i == len(products) - 1:
                            # No, añadamos el nuevo registro.
                            products.append([product, totalTax])

        '''
        Una vez tenemos la lista en el formato correcto, procedemos a ordenarla, para
        ello empezamos metiendo el primer registro en una variable aparte, y a partir de ahí
        pillamos los demas registros y los comparamos con los que ya estan en la variable
        secundaria, consiguiendo de esta manera una lista en orden ascendiente.
        '''

        # Vale, ahora tengo una lista con todos los registros, toca ordenarlos.
        # Revisemos los registros uno por uno.
        for i in range(len(products)):
            # Necesitaré un listado aparte para poder ordenarlos.
            # El listado tiene registros?
            if len(orderedProducts) == 0:
                # No, pongamos el primero.
                orderedProducts.append(products[i])
            else:
                # Si, habra que revisarlos uno a uno para ver donde va.
                for y in range(len(orderedProducts)):
                    # Este producto tiene menos impuesto que el ya registrado?
                    if products[i][1] < orderedProducts[y][1]:
                        # Si, pongamoslo delante.
                        orderedProducts.insert(y, products[i])
                        break
                    # Hemos llegado al final del listado, esta claro que su impuesto es el más grande.
                    if y == len(orderedProducts) - 1:
                        # Pongamoslo al final de la lista.
                        orderedProducts.append(products[i])

        '''
        En caso de querer lista en orden descendiente, esta pequeña funcion se encargará de invertirla.
        '''      
        # Espera, la lista era descendiente?          
        if order_type == 1:
            # Ah, si, bueno, no pasa nada, la invierto y ya está.
            orderedProducts.reverse()

        # Enviaré la lista al jefe.
        return tuple(orderedProducts)

    def show(self):
        # Do not change this method
        print("Bills")
        for bill in self.bills:
            bill.print()
