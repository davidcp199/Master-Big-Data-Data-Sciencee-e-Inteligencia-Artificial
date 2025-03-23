import pandas as pd

def count_movies_by_year(df: pd.DataFrame, year: int) -> int:
    """
    Cuenta la cantidad de películas únicas (sin títulos repetidos) realizadas en un año específico.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame que contiene los datos de las películas.
    year : int
        Año a filtrar en la columna 'title_year'.

    Returns
    -------
    int
        Número de películas realizadas en el año especificado.
    """
    # Elimina duplicados en 'movie_title'
    df_unique = df.drop_duplicates(subset="movie_title")
    # Filtra las películas del año indicado
    movies_in_year = df_unique[df_unique["title_year"] == year]
    # Devuelve la cantidad de filas (películas) encontradas
    return movies_in_year.shape[0]

if __name__ == "__main__":
    # Cargar el DataFrame desde un CSV (ajusta el nombre del archivo según corresponda)
    df = pd.read_csv("datain/movie_data.csv")
    # Solicitar el año al usuario
    year_input = int(input("Ingrese el año: "))
    count = count_movies_by_year(df, year_input)
    print(f"Cantidad de películas realizadas en {year_input}: {count}")
