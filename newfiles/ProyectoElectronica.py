class ProyectoElectronica():
    def __init__(self, nombreproyecto,bbdd):
        self.nombre = nombreproyecto
        self.descripcion, self.relevancia, self.presupuesto, self.numeroempleadosHW, self.numeroempleadosFW, self.numeroempleadosSW, self.numeroempleadosProduccion, self.numeroempleadosTesting, self.numeroempreadosMecanica, self.numeroepleadosGestion, self.duracionmeses, self.dificultad,self.tipo, self.producto,self.numeroproductos =  bbdd.obtener_informacion_proyecto_electronica(nombreproyecto)
        self.porcentajefinalizacion=100
        self.finalizado=False
        # relevancia (entre 0 y 0.01)

    def mostrar_informacion(self):
        print(f"Nombre Proyecto: {self.tipnombreo}")

    def indiceproduccionmes(self,empleados_empresa):

        empleadosHW = empleados_empresa.get("numeroempleadosHW")
        empleados_empresa["numeroempleadosHW"] = empleadosHW - self.numeroempleadosHW
        if empleados_empresa.get("numeroempleadosHW") < 0:
            empleados_empresa["numeroempleadosHW"] = 0
            empleadosHWFinal=empleadosHW
        else:
            empleadosHWFinal=self.numeroempleadosHW

        empleadosFW = empleados_empresa.get("numeroempleadosFW")
        empleados_empresa["numeroempleadosFW"] = empleadosFW - self.numeroempleadosFW
        if empleados_empresa.get("numeroempleadosFW") < 0:
            empleados_empresa["numeroempleadosFW"] = 0
            empleadosFWFinal=empleadosFW
        else:
            empleadosFWFinal=self.numeroempleadosFW

        empleadosSW = empleados_empresa.get("numeroempleadosSW")
        empleados_empresa["numeroempleadosSW"] = empleadosSW - self.numeroempleadosSW
        if empleados_empresa.get("numeroempleadosSW") < 0:
            empleados_empresa["numeroempleadosSW"] = 0
            empleadosSWFinal=empleadosSW
        else:
            empleadosSWFinal=self.numeroempleadosSW

        empleadosProduccion = empleados_empresa.get("numeroempleadosProduccion")
        empleados_empresa["numeroempleadosProduccion"] = empleadosProduccion - self.numeroempleadoProduccion
        if empleados_empresa.get("numeroempleadosProduccion") < 0:
            empleados_empresa["numeroempleadosProduccion"] = 0
            empleadosProduccionFinal=empleadosProduccion
        else:
            empleadosProduccionFinal=self.numeroempleadosProduccion

        empleadosTesting = empleados_empresa.get("numeroempleadosTesting")
        empleados_empresa["numeroempleadosTesting"] = empleadosTesting - self.numeroempleadosTesting
        if empleados_empresa.get("numeroempleadosTesting") < 0:
            empleados_empresa["numeroempleadosTesting"] = 0
            empleadosTestingFinal=empleadosTesting
        else:
            empleadosTestingFinal=self.numeroempleadosTesting

        empleadosMecanica = empleados_empresa.get("numeroempleadosMecanica")
        empleados_empresa["numeroempleadosMecanica"] = empleadosMecanica - self.numeroempleadosMecanica
        if empleados_empresa.get("numeroempleadosMecanica") < 0:
            empleados_empresa["numeroempleadosMecanica"] = 0
            empleadosMecanicaFinal=empleadosMecanica
        else:
            empleadosMecanicaFinal=self.numeroempreadosMecanica

        empleadosGestion = empleados_empresa.get("numeroempleadosGestion")
        empleados_empresa["numeroempleadosGestion"] = empleadosGestion - self.numeroempleadosGestion
        if empleados_empresa.get("numeroempleadosGestion") < 0:
            empleados_empresa["numeroempleadosGestion"] = 0
            empleadosGestionFinal=empleadosGestion
        else:
            empleadosGestionFinal=self.numeroempleadosGestion

        numeroempleadosutilizados=empleadosHWFinal+empleadosFWFinal+empleadosSWFinal+empleadosProduccionFinal+empleadosTestingFinal+empleadosMecanicaFinal+empleadosGestionFinal
        numeroempleadosnecesarios=self.numeroempleadosHW + self.numeroempleadosFW + self.numeroempleadosSW + self.numeroempleadosProduccion + self.numeroempleadosTesting + self.numeroempreadosMecanica + self.numeroepleadosGestion
        indice=numeroempleadosutilizados/numeroempleadosnecesarios
        return empleados_empresa, indice
