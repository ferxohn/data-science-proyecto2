#!/usr/bin/env python
# coding: utf-8

# Proyecto 2

import pandas as pd
import matplotlib.pyplot as plt

# Importar el conjunto de datos al entorno
db = pd.read_csv('synergy_logistics_database.csv')
db.head()

# Opción 1) Rutas de importación y exportación. Synergy logistics está considerando la posibilidad de enfocar sus esfuerzos en las 10 rutas más demandadas. Acorde a los flujos de importación y exportación, ¿cuáles son esas 10 rutas? ¿le conviene implementar esa estrategia? ¿porqué?

# Agrupar los resultados por la direccion del flujo
routes = db[['direction', 'origin', 'destination']].value_counts()
routes = pd.DataFrame(routes).groupby('direction')

# Rutas de exportacion mas demandadas
exports_head = routes.get_group('Exports').head(n = 10)
exports_head.plot(kind = 'bar')
plt.savefig('opcion_1_exports.jpeg', bbox_inches='tight')
plt.show()

# Rutas de importacion mas demandadas
imports_head = routes.get_group('Imports').head(n = 10)
imports_head.plot(kind = 'bar')
plt.savefig('opcion_1_imports.jpeg', bbox_inches='tight')
plt.show()

# Opción 2) Medio de transporte utilizado. ¿Cuáles son los 3 medios de transporte más importantes para Synergy logistics considerando el valor de las importaciones y exportaciones? ¿Cuál es medio de transporte que podrían reducir?

# Agrupar los resultados por el medio de transporte y sumar su valor total, ordenando de forma descendente
transport = db[['direction', 'transport_mode', 'total_value']].groupby(['direction', 'transport_mode']).sum()
transport = transport.sort_values('total_value', ascending = False)

# Ordenar los medios de transporte por su valor (en general)
transport.droplevel(0).groupby('transport_mode').sum().sort_values('total_value', ascending = False).plot(kind = 'bar')
plt.savefig('opcion_2_main.jpeg', bbox_inches='tight')
plt.show()

# Agrupar los transportes por direccion
transport = transport.groupby('direction')

# Obtener los medios de transporte para las exportaciones
transport.get_group('Exports').plot(kind = 'bar')
plt.savefig('opcion_2_exports.jpeg', bbox_inches='tight')
plt.show()

# Obtener los medios de transporte para las importaciones
transport.get_group('Imports').plot(kind = 'bar')
plt.savefig('opcion_2_imports.jpeg', bbox_inches='tight')
plt.show()

# Opción 3) Valor total de importaciones y exportaciones. Si Synergy Logistics quisiera enfocarse en los países que le generan el 80% del valor de las exportaciones e importaciones ¿en qué grupo de países debería enfocar sus esfuerzos?

# Obtener el total de las importaciones y exportaciones
total_values = db[['direction', 'total_value']].groupby(['direction']).sum()
total_values

# Separar los valores anteriores en variables
total_exports = total_values.iloc[0]['total_value']
total_imports = total_values.iloc[1]['total_value']

# Obtener la suma de valores totales por direccion de flujo y paises, ordenados de forma descendente
values_per_countries = db[['direction', 'origin', 'destination', 'total_value']].groupby(['direction', 'origin', 'destination']).sum()    .sort_values('total_value', ascending = False).groupby(['direction'])

# Obtener los paises cuyas exportaciones representa el 80% del total de exportaciones
exports = values_per_countries.get_group('Exports')
exports = exports[exports.cumsum()['total_value'] <= total_exports * 0.8].reset_index()

# Obtener los paises cuyas importaciones representa el 80% del total de importaciones
imports = values_per_countries.get_group('Imports')
imports = imports[imports.cumsum()['total_value'] <= total_imports * 0.8].reset_index()

# Obtener las rutas en comun de importaciones y exportaciones
exports_countries = exports[['origin', 'destination']]
imports_countries = imports[['origin', 'destination']]
exports_countries.join(imports_countries.set_index(['origin', 'destination']), on = ['origin', 'destination'], how = 'inner')