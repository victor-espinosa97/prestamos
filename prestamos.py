from datetime import datetime, timedelta

def registrar_prestamo(usuarios, items, prestamos):
    doc = input("Documento: ")

    usuario = next((u for u in usuarios if u["doc"] == doc), None)
    if not usuario:
        print("Usuario no existe ❌")
        return

    disponibles = [i for i in items if i["disponible"]]

    for i in disponibles:
        print(i["id"], i["nombre"])

    item_id = input("ID del item: ")
    item = next((i for i in items if i["id"] == item_id and i["disponible"]), None)

    if not item:
        print("Item no disponible ❌")
        return

    inicio = datetime.now()
    fin = inicio + timedelta(days=usuario["tiempo"])

    prestamos.append({
        "usuario": doc,
        "item": item_id,
        "inicio": str(inicio),
        "fin": str(fin),
        "activo": True
    })

    item["disponible"] = False
    usuario["prestamos"] += 1

    print("Préstamo registrado ✔")


def devolver(prestamos, items):
    doc = input("Documento: ")

    activo = next((p for p in prestamos if p["usuario"] == doc and p["activo"]), None)

    if not activo:
        print("No tiene préstamos ❌")
        return

    activo["activo"] = False

    item = next(i for i in items if i["id"] == activo["item"])
    item["disponible"] = True

    with open(f"{doc}_{item['id']}.txt", "w") as f:
        f.write("Certificado devolución\n")
        f.write(str(activo))

    print("Devolución registrada ✔")