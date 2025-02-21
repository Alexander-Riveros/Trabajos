# Definición del patrón Singleton para garantizar que solo haya una instancia de la clase
class Singleton:
    _instance = None  # Variable de clase para almacenar la única instancia

    def __new__(cls):  # Método especial para la creación de instancias
        if cls._instance is None:  # Si no existe una instancia previa
            cls._instance = super(Singleton, cls).__new__(cls)  # Se crea una nueva instancia
        return cls._instance  # Retorna la instancia única existente

# Clase DatabaseConnection que hereda de Singleton
class DatabaseConnection(Singleton):
    def connect(self):
        return "Conectado a la base de datos"  # Simula una conexión a la base de datos

# Definición del patrón Factory para la creación de reportes
class ReportFactory:
    def create_report(self, report_type):  # Método para crear un reporte según el tipo solicitado
        if report_type == "PDF":  # Si el tipo es PDF
            return PDFReport()  # Retorna una instancia de PDFReport
        elif report_type == "HTML":  # Si el tipo es HTML
            return HTMLReport()  # Retorna una instancia de HTMLReport
        else:
            raise ValueError("Tipo de reporte desconocido")  # Lanza un error si el tipo es inválido

# Clase para la generación de reportes en PDF
class PDFReport:
    def generate(self):
        return "Generando reporte en PDF"  # Simula la generación de un reporte en PDF

# Clase para la generación de reportes en HTML
class HTMLReport:
    def generate(self):
        return "Generando reporte en HTML"  # Simula la generación de un reporte en HTML

# Implementación del patrón Facade para simplificar la generación de reportes
class ReportFacade:
    def __init__(self):
        self.db = DatabaseConnection()  # Obtiene la única instancia de DatabaseConnection (Singleton)
        self.factory = ReportFactory()  # Crea una instancia de ReportFactory para generar reportes

    def generate_report(self, report_type):  # Método para generar un reporte
        print(self.db.connect())  # Conecta a la base de datos (simulado)
        report = self.factory.create_report(report_type)  # Crea un reporte del tipo solicitado
        return report.generate()  # Genera y retorna el reporte

# Uso del patrón Facade para simplificar la interacción con el sistema
facade = ReportFacade()  # Se crea una instancia de ReportFacade
print(facade.generate_report("PDF"))  # Genera y muestra un reporte en PDF
print(facade.generate_report("HTML"))  # Genera y muestra un reporte en HTML
