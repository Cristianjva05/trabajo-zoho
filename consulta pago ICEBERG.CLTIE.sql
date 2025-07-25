--------------------- buscar pagos-------------------------

SELECT c.*, rowid FROM ICEBERG.CLTIENE_360_FUERZA_COMERCIAL c  WHERE C.NUMERODOCUMENTO IN ('1022946763');
------------------------- buscar correos -------------------------
select DIR_EMAIL,t.*, rowid from SINU.bas_tercero t WHERE --buscar datos por cedula
t.NUM_IDENTIFICACION  = '1233907772';
---------------------CREACION DE CORREOS ZOHO-------------------------
SELECT * FROM ICEBERG.CUNT_LDAP_TRANSACCIONES c WHERE C.NUM_IDENTIFICACION IN ('1032378807');
