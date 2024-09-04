import life_table_core.life_table_func

if __name__ == '__main__':
    df = life_table_core.life_table_func.life_table(2, 2, 1000)
    # df is a pandas.DataFrame
    print(df)
