import requests
from bs4 import BeautifulSoup


def get_all_links_courses():
    url = "https://kodekloud.com/courses/"
    # Crea un diccionario con los datos del formulario
    index = 1
    list_responses = []
    ok_response = False
    while not ok_response and index < 10:
        try:
            print(index)
            form_data = {
                "current_page": str(index)
            }
            # Realiza la solicitud HTTP POST con los datos del formulario
            response = requests.post(url, data=form_data)
            if response.status_code != 200:
                ok_response = True
                break
            list_responses.append(response)
            index += 1
        except Exception as e:
            print("Error en el ciclo while: ")
            print(e)
            break
    matching_links = []
    for response_ in list_responses:
        # Parsea la respuesta con Beautiful Soup
        try:
            soup = BeautifulSoup(response_.content, "html.parser")
            all_links = soup.find_all("a")
            # Crea una lista vacía para almacenar los links que coinciden con los criterios de búsqueda

            # Itera sobre todos los elementos "a" encontrados
            for link in all_links:
                # Verifica si el atributo "href" contiene la palabra "kodekloud.com"
                if link.has_attr("href") and link["href"].startswith("https://kodekloud.com/courses/"):
                    # Verifica si la clase "bb-cover-wrap" está en la lista de clases del elemento
                    classes = link.get("class", [])
                    if "bb-cover-wrap" in classes:
                        # Si el link coincide con los criterios de búsqueda, agrega su valor "href" a la lista
                        matching_links.append(link["href"])
            # Imprime la lista de links que coinciden con los criterios de búsqueda
        except Exception as e:
            print("Error al obtener la lista loca")
            print(e)
        print("Primera lista:")
        print(len(matching_links))
        print(matching_links)
        print("Lista sin repetidos:")

        conjunto_sin_repetidos = set(matching_links)

        # Convertimos el conjunto de nuevo en una lista
        lista_sin_repetidos = list(conjunto_sin_repetidos)

        # Imprimimos la lista resultante sin elementos repetidos
        print(len(lista_sin_repetidos))
        print(lista_sin_repetidos)
        return matching_links


get_all_links_courses()
