/*==============================================================*/
/* DBMS name:      PostgreSQL 8                                 */
/* Created on:     1/25/2025 11:52:00 AM                        */
/*==============================================================*/



/*==============================================================*/
/* Table: CATEGORIA                                             */
/*==============================================================*/
create table CATEGORIA (
   ID_CATEGORIA         SERIAL               not null,
   NOMBRE_CATEGORIA     VARCHAR(100)         not null,
   DESCRIPCION_CATEGORIA VARCHAR(1024)        not null,
   constraint PK_CATEGORIA primary key (ID_CATEGORIA)
);

/*==============================================================*/
/* Index: CATEGORIA_PK                                          */
/*==============================================================*/
create unique index CATEGORIA_PK on CATEGORIA (
ID_CATEGORIA
);

/*==============================================================*/
/* Table: CIUDAD                                                */
/*==============================================================*/
create table CIUDAD (
   ID_CIUDAD            SERIAL               not null,
   ID_PROVINCIA         INT4                 not null,
   NOMBRE_CIUDAD        VARCHAR(100)         not null,
   constraint PK_CIUDAD primary key (ID_CIUDAD)
);

/*==============================================================*/
/* Index: CIUDAD_PK                                             */
/*==============================================================*/
create unique index CIUDAD_PK on CIUDAD (
ID_CIUDAD
);

/*==============================================================*/
/* Index: PROVINCIA_CIUDAD_FK                                   */
/*==============================================================*/
create  index PROVINCIA_CIUDAD_FK on CIUDAD (
ID_PROVINCIA
);

/*==============================================================*/
/* Table: CLIENTE                                               */
/*==============================================================*/
create table CLIENTE (
   ID_CLIENTE           SERIAL               not null,
   NOMBRE               VARCHAR(100)         not null,
   TELEFONO             VARCHAR(13)          not null,
   CORREO               VARCHAR(50)          not null,
   CONTRASENA           VARCHAR(32)          not null,
   constraint PK_CLIENTE primary key (ID_CLIENTE)
);

/*==============================================================*/
/* Index: CLIENTE_PK                                            */
/*==============================================================*/
create unique index CLIENTE_PK on CLIENTE (
ID_CLIENTE
);

/*==============================================================*/
/* Table: COMPRA                                                */
/*==============================================================*/
create table COMPRA (
   ID_COMPRA            SERIAL               not null,
   ID_CLIENTE           INT4                 not null,
   ID_DIRECCION         INT4                 not null,
   IMPUESTOS            DECIMAL(3,2)         not null,
   IMPORTE              DECIMAL(6,2)         not null,
   PRECIO_TOTAL         DECIMAL(6,2)         not null,
   constraint PK_COMPRA primary key (ID_COMPRA)
);

/*==============================================================*/
/* Index: COMPRA_PK                                             */
/*==============================================================*/
create unique index COMPRA_PK on COMPRA (
ID_COMPRA
);

/*==============================================================*/
/* Index: CLIENTE_COMPRA_FK                                     */
/*==============================================================*/
create  index CLIENTE_COMPRA_FK on COMPRA (
ID_CLIENTE
);

/*==============================================================*/
/* Index: DIRECCION_COMPRA_FK                                   */
/*==============================================================*/
create  index DIRECCION_COMPRA_FK on COMPRA (
ID_DIRECCION
);

/*==============================================================*/
/* Table: DETALLE_COMPRA                                        */
/*==============================================================*/
create table DETALLE_COMPRA (
   ID_PRODUCTO          INT4                 not null,
   ID_COMPRA            INT4                 not null,
   CANTIDAD             INT4                 not null,
   PRECIO_UNITARIO      DECIMAL(6,2)         not null,
   SUBTOTAL             DECIMAL(6,2)         not null,
   constraint PK_DETALLE_COMPRA primary key (ID_PRODUCTO, ID_COMPRA)
);

/*==============================================================*/
/* Index: DETALLE_COMPRA_PK                                     */
/*==============================================================*/
create unique index DETALLE_COMPRA_PK on DETALLE_COMPRA (
ID_PRODUCTO,
ID_COMPRA
);

/*==============================================================*/
/* Index: RELATIONSHIP_13_FK                                    */
/*==============================================================*/
create  index RELATIONSHIP_13_FK on DETALLE_COMPRA (
ID_COMPRA
);

/*==============================================================*/
/* Index: DETALLE_PRODUCTO_FK                                   */
/*==============================================================*/
create  index DETALLE_PRODUCTO_FK on DETALLE_COMPRA (
ID_PRODUCTO
);

/*==============================================================*/
/* Table: DIRECCION                                             */
/*==============================================================*/
create table DIRECCION (
   ID_DIRECCION         SERIAL               not null,
   ID_CIUDAD            INT4                 not null,
   DIRECCION_PRINCIPAL  VARCHAR(100)         not null,
   DIRECCION_SECUNDARIA VARCHAR(100)         not null,
   CODIGO_POSTAL        VARCHAR(10)          not null,
   constraint PK_DIRECCION primary key (ID_DIRECCION)
);

/*==============================================================*/
/* Index: DIRECCION_PK                                          */
/*==============================================================*/
create unique index DIRECCION_PK on DIRECCION (
ID_DIRECCION
);

/*==============================================================*/
/* Index: CIUDAD_DIRECCION_FK                                   */
/*==============================================================*/
create  index CIUDAD_DIRECCION_FK on DIRECCION (
ID_CIUDAD
);

/*==============================================================*/
/* Table: GIFT_CARD                                             */
/*==============================================================*/
create table GIFT_CARD (
   ID_GIFT              SERIAL               not null,
   ID_METODOPAGO        INT4                 not null,
   SALDO                DECIMAL(6,2)         not null,
   FECHA_EMISION        DATE                 not null,
   FECHA_EXPEDICION     DATE                 not null,
   constraint PK_GIFT_CARD primary key (ID_GIFT)
);

/*==============================================================*/
/* Index: GIFT_CARD_PK                                          */
/*==============================================================*/
create unique index GIFT_CARD_PK on GIFT_CARD (
ID_GIFT
);

/*==============================================================*/
/* Index: METODOPAGO_GIFTCARD_FK                                */
/*==============================================================*/
create  index METODOPAGO_GIFTCARD_FK on GIFT_CARD (
ID_METODOPAGO
);

/*==============================================================*/
/* Table: METODO_DE_PAGO                                        */
/*==============================================================*/
create table METODO_DE_PAGO (
   ID_METODOPAGO        SERIAL               not null,
   ID_COMPRA            INT4                 not null,
   TIPO_PAGO            VARCHAR(100)         not null,
   constraint PK_METODO_DE_PAGO primary key (ID_METODOPAGO)
);

/*==============================================================*/
/* Index: METODO_DE_PAGO_PK                                     */
/*==============================================================*/
create unique index METODO_DE_PAGO_PK on METODO_DE_PAGO (
ID_METODOPAGO
);

/*==============================================================*/
/* Index: METODOPAGO_COMPRA_FK                                  */
/*==============================================================*/
create  index METODOPAGO_COMPRA_FK on METODO_DE_PAGO (
ID_COMPRA
);

/*==============================================================*/
/* Table: PAIS                                                  */
/*==============================================================*/
create table PAIS (
   ID_PAIS              SERIAL               not null,
   NOMBRE_PAIS          VARCHAR(50)          not null,
   constraint PK_PAIS primary key (ID_PAIS)
);

/*==============================================================*/
/* Index: PAIS_PK                                               */
/*==============================================================*/
create unique index PAIS_PK on PAIS (
ID_PAIS
);

/*==============================================================*/
/* Table: PRODUCTO                                              */
/*==============================================================*/
create table PRODUCTO (
   ID_PRODUCTO          SERIAL               not null,
   ID_CATEGORIA         INT4                 not null,
   ID_PROVEEDOR         INT4                 not null,
   NOMBRE               VARCHAR(100)         not null,
   DESCRIPCION          VARCHAR(1024)        not null,
   PRECIO               DECIMAL(6,2)         not null,
   DESCUENTO            INT4                 not null,
   STOCK                INT4                 not null,
   CALIFICACION         DECIMAL(1,1)         not null,
   IMAGEN               VARCHAR(1024)        not null,
   constraint PK_PRODUCTO primary key (ID_PRODUCTO)
);

/*==============================================================*/
/* Index: PRODUCTO_PK                                           */
/*==============================================================*/
create unique index PRODUCTO_PK on PRODUCTO (
ID_PRODUCTO
);

/*==============================================================*/
/* Index: CATEGORIA_PRODUCTO_FK                                 */
/*==============================================================*/
create  index CATEGORIA_PRODUCTO_FK on PRODUCTO (
ID_CATEGORIA
);

/*==============================================================*/
/* Index: PROVEEDOR_PRODUCTO_FK                                 */
/*==============================================================*/
create  index PROVEEDOR_PRODUCTO_FK on PRODUCTO (
ID_PROVEEDOR
);

/*==============================================================*/
/* Table: PROVEEDOR                                             */
/*==============================================================*/
create table PROVEEDOR (
   ID_PROVEEDOR         SERIAL               not null,
   NOMBRE               VARCHAR(100)         not null,
   DESCRIPCION_PROVEEDOR VARCHAR(1024)        not null,
   TELEFONO_PROVEEDOR   VARCHAR(13)          not null,
   CORREO_PROVEEDOR     VARCHAR(100)         not null,
   constraint PK_PROVEEDOR primary key (ID_PROVEEDOR)
);

/*==============================================================*/
/* Index: PROVEEDOR_PK                                          */
/*==============================================================*/
create unique index PROVEEDOR_PK on PROVEEDOR (
ID_PROVEEDOR
);

/*==============================================================*/
/* Table: PROVINCIA                                             */
/*==============================================================*/
create table PROVINCIA (
   ID_PROVINCIA         SERIAL               not null,
   ID_PAIS              INT4                 not null,
   NOMBRE_PROVINCIA     VARCHAR(100)         not null,
   constraint PK_PROVINCIA primary key (ID_PROVINCIA)
);

/*==============================================================*/
/* Index: PROVINCIA_PK                                          */
/*==============================================================*/
create unique index PROVINCIA_PK on PROVINCIA (
ID_PROVINCIA
);

/*==============================================================*/
/* Index: PAIS_PROVINCIA_FK                                     */
/*==============================================================*/
create  index PAIS_PROVINCIA_FK on PROVINCIA (
ID_PAIS
);

/*==============================================================*/
/* Table: RASTREO                                               */
/*==============================================================*/
create table RASTREO (
   ID_RASTREO           SERIAL               not null,
   ID_COMPRA            INT4                 not null,
   FECHA_ENVIO          DATE                 not null,
   ESTADO_RASTREO       BOOL                 not null,
   FECHA_ENTREGA        DATE                 not null,
   constraint PK_RASTREO primary key (ID_RASTREO)
);

/*==============================================================*/
/* Index: RASTREO_PK                                            */
/*==============================================================*/
create unique index RASTREO_PK on RASTREO (
ID_RASTREO
);

/*==============================================================*/
/* Index: RASTREO_COMPRA_FK                                     */
/*==============================================================*/
create  index RASTREO_COMPRA_FK on RASTREO (
ID_COMPRA
);

/*==============================================================*/
/* Table: TARJETA                                               */
/*==============================================================*/
create table TARJETA (
   NUM_TARJETA          VARCHAR(16)          not null,
   ID_METODOPAGO        INT4                 not null,
   NOMBRE               VARCHAR(100)         not null,
   FECHA_VENCIMIENTO    VARCHAR(5)           not null,
   CVV                  VARCHAR(3)           not null,
   constraint PK_TARJETA primary key (NUM_TARJETA)
);

/*==============================================================*/
/* Index: TARJETA_PK                                            */
/*==============================================================*/
create unique index TARJETA_PK on TARJETA (
NUM_TARJETA
);

/*==============================================================*/
/* Index: METODOPAGO_TARJETA_FK                                 */
/*==============================================================*/
create  index METODOPAGO_TARJETA_FK on TARJETA (
ID_METODOPAGO
);

alter table CIUDAD
   add constraint FK_CIUDAD_PROVINCIA_PROVINCI foreign key (ID_PROVINCIA)
      references PROVINCIA (ID_PROVINCIA)
      on delete restrict on update restrict;

alter table COMPRA
   add constraint FK_COMPRA_CLIENTE_C_CLIENTE foreign key (ID_CLIENTE)
      references CLIENTE (ID_CLIENTE)
      on delete restrict on update restrict;

alter table COMPRA
   add constraint FK_COMPRA_DIRECCION_DIRECCIO foreign key (ID_DIRECCION)
      references DIRECCION (ID_DIRECCION)
      on delete restrict on update restrict;

alter table DETALLE_COMPRA
   add constraint FK_DETALLE__DETALLE_P_PRODUCTO foreign key (ID_PRODUCTO)
      references PRODUCTO (ID_PRODUCTO)
      on delete restrict on update restrict;

alter table DETALLE_COMPRA
   add constraint FK_DETALLE__RELATIONS_COMPRA foreign key (ID_COMPRA)
      references COMPRA (ID_COMPRA)
      on delete restrict on update restrict;

alter table DIRECCION
   add constraint FK_DIRECCIO_CIUDAD_DI_CIUDAD foreign key (ID_CIUDAD)
      references CIUDAD (ID_CIUDAD)
      on delete restrict on update restrict;

alter table GIFT_CARD
   add constraint FK_GIFT_CAR_METODOPAG_METODO_D foreign key (ID_METODOPAGO)
      references METODO_DE_PAGO (ID_METODOPAGO)
      on delete restrict on update restrict;

alter table METODO_DE_PAGO
   add constraint FK_METODO_D_METODOPAG_COMPRA foreign key (ID_COMPRA)
      references COMPRA (ID_COMPRA)
      on delete restrict on update restrict;

alter table PRODUCTO
   add constraint FK_PRODUCTO_CATEGORIA_CATEGORI foreign key (ID_CATEGORIA)
      references CATEGORIA (ID_CATEGORIA)
      on delete restrict on update restrict;

alter table PRODUCTO
   add constraint FK_PRODUCTO_PROVEEDOR_PROVEEDO foreign key (ID_PROVEEDOR)
      references PROVEEDOR (ID_PROVEEDOR)
      on delete restrict on update restrict;

alter table PROVINCIA
   add constraint FK_PROVINCI_PAIS_PROV_PAIS foreign key (ID_PAIS)
      references PAIS (ID_PAIS)
      on delete restrict on update restrict;

alter table RASTREO
   add constraint FK_RASTREO_RASTREO_C_COMPRA foreign key (ID_COMPRA)
      references COMPRA (ID_COMPRA)
      on delete restrict on update restrict;

alter table TARJETA
   add constraint FK_TARJETA_METODOPAG_METODO_D foreign key (ID_METODOPAGO)
      references METODO_DE_PAGO (ID_METODOPAGO)
      on delete restrict on update restrict;

