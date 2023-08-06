# bccr

**Una API de Python para descargar datos del Banco Central de Costa Rica**

El propósito de este paquete es proveer herramientas para buscar y descargar indicadores publicados por el Banco Central de Costa Rica (BCCR_).


El código fuente está disponible en Github_.

El paquete ofrece dos clases para buscar datos y descargarlos:

+ ServicioWeb_: descarga indicadores individuales. Es necesario suscribirse_ previamente.
+ PaginaWeb_: descarga cuadros individuales (algunos con un solo indicador, otros con varios).

Los datos son ofrecidos en formato de tabla de datos de pandas_.

AVISO: Este paquete no es un producto oficial de BCCR. El autor lo provee para facilitar el manejo de datos, pero no ofrece ninguna garantía acerca de su correcto funcionamiento. 


.. _BCCR: https://www.bccr.fi.cr/seccion-indicadores-economicos/indicadores-económicos
.. _Github: https://github.com/randall-romero/bccr
.. _suscribirse: https://www.bccr.fi.cr/seccion-indicadores-economicos/servicio-web
.. _ServicioWeb: http://randall-romero.com/demo-bccr-servicioweb/
.. _PaginaWeb: http://randall-romero.com/demo-bccr-paginaweb/ 
.. _pandas: https://pandas.pydata.org/
