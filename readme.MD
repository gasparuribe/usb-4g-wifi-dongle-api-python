Este codigo lo use para controlar algunas caracteristicas de mi usb Sim 3g/4g wifi modem.

Con el codigo se puede:
1. Encender y apagar coneccion movil
2. Encender y apagar coneccion wifi
3. Obtener mensajes (leidos y sin leer)
4. Obtener informacion respecto cantidad de mensajes
5. Enviar SMS
6. Eliminar SMS

Cosas que considero agregar pero aun no hago:
<ul>
<li>Informacion de velocidad internet</li>
<li>Control e informacion tarjeta SD</li>
<li>Control e informacion señal movil</li>
<li>Control e informacion wifi completo (aun no quiero usar ese wifi...)</li>
<li>Control e informacion 4gusb extendido</li>
</ul>


Probe el codigo con python3.


En mi caso era un usb de la compañia Movistar y no tenia una marca o modelo donde encontrar informacion de el.

La informacion que encontre del disposivo:
<ul>
<li>Versión hardware (en interfaz web): F232E_v3.0_RR_FX</li>
<li>Versión software (en interfaz web): XFNJ_B03P14_F232E_V3.0_RR_FX_MOVISTAR_P009</li>
<li>
  Chips en dispositivo:
  <ol>
    <li>... MICRO FM25LS01 ...</li>
    <li>ZXIC ZX297520V3 0109 FAPDS ...</li>
    <li>RTL8189ES KBU20H1 ...</li>
    <li>ZXIC ZX234220A1 P1 0107HT ...</li>
    <li>RADROCK RR88643-21 P0840222J ...</li>
  </ol>
</li>

</ul>

Lo que utilice para encontrar los siguientes enlaces que tenian la informacion necesaria en realidad fue la
busqueda de una variable llamada "zte_web_ui_is_test" encontrada en el archivo "192.168.0.1/js/main.js"


URLS importantes que use para apender como escribir este codigo y más:

https://www.development-cycle.com/2017/04/27/zte-mf823-inside/

https://github.com/paulo-correia/ZTE_API_and_Hack

https://www.slideshare.net/phdays/4g-modem

http://blog.asiantuntijakaveri.fi/2017/03/backdoor-and-root-shell-on-zte-mf286.html


Un Script Bash enfocado en SMS que probe en linux y funciono con pequeñas modificaciones de compatibilidad.
https://gist.github.com/mariodian/65641792700d237d30f3f47d24c746e0
