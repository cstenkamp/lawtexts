import os
P = os.path.join(os.getcwd(),'Definitions/html_resources/')


class Definitions():
	def __init__(self):
		pass 

	def maschine(self):
		txt = """
„Maschine“

— eine mit einem anderen Antriebssystem als der unmittelbar eingesetzten
	menschlichen oder tierischen Kraft ausgestattete oder dafür vorgesehene 
	Gesamtheit miteinander verbundener Teile oder Vorrichtungen, von denen 
	mindestens eines bzw. eine beweglich ist und die für eine bestimmte 
	Anwendung zusammengefügt sind;
— eine Gesamtheit im Sinne des ersten Gedankenstrichs, der lediglich die Teile
	fehlen, die sie mit ihrem Einsatzort oder mit ihren Energie- und 
	Antriebsquellen verbinden;
— eine einbaufertige Gesamtheit im Sinne des ersten und zweiten 
	Gedankenstrichs, die erst nach Anbringung auf einem Beförderungsmittel oder 
	Installation in einem Gebäude oder Bauwerk funktionsfähig ist;
— eine Gesamtheit von Maschinen im Sinne des ersten, zweiten und 
	dritten Gedankenstrichs oder von unvollständigen Maschinen im Sinne des 
	Buchstabens g, die, damit sie zusammenwirken, so angeordnet sind und 
	betätigt werden, dass sie als Gesamtheit funktionieren;
— eine Gesamtheit miteinander verbundener Teile oder Vorrichtungen, von denen
	mindestens eines bzw. eine beweglich ist und die für Hebevorgänge 
	zusammengefügt sind und deren einzige Antriebsquelle die unmittelbar 
	eingesetzte menschliche Kraft ist;
	"""
		html_source = P+'maschine.html'
		return txt, html_source

	def ausweAusr(self):
		txt="""
„auswechselbare Ausrüstung“ 
	eine Vorrichtung, die der Bediener einer Maschine oder Zugmaschine nach 
	deren Inbetriebnahme selbst an ihr anbringt, um ihre Funktion zu ändern 
	oder zu erweitern, sofern diese Ausrüstung kein Werkzeug ist;
		"""
		html_source = P+'auswAusr.html'
		return txt, html_source

	def sichBaut(self):
		txt="""	
„Sicherheitsbauteil“ ein Bauteil,
	— das zur Gewährleistung einer Sicherheitsfunktion dient,
	— gesondert in Verkehr gebracht wird,
	— dessen Ausfall und/oder Fehlfunktion die Sicherheit von Personen 
	  gefährdet und
	— das für das Funktionieren der Maschine nicht erforderlich ist oder durch
	  für das Funktionieren der Maschine übliche Bauteile ersetzt werden kann.

Eine nicht erschöpfende Liste von Sicherheitsbauteilen findet sich in Anhang V, der gemäß Artikel 8 Absatz 1 Buchstabe a aktualisiert werden kann;
		"""
		html_source = P+'sichBaut.html'
		return txt, html_source

	def lastMit(self):
		txt="""
„Lastaufnahmemittel“ 
	ein nicht zum Hebezeug gehörendes Bauteil oder Ausrüstungsteil, das das 
	Ergreifen der Last ermöglicht und das zwischen Maschine und Last oder an 
	der Last selbst angebracht wird oder das dazu bestimmt ist, ein integraler 
	Bestandteil der Last zu werden, und das gesondert in Verkehr gebracht wird; 
	als Lastaufnahmemittel gelten auch Anschlagmittel und ihre Bestandteile;
		"""
		html_source = P+'lastMit.html'
		return txt, html_source

	def ketten(self):
		txt = """
„Ketten, Seile und Gurte“
	für Hebezwecke als Teil von Hebezeugen oder Lastaufnahmemitteln entwickelte 
	und hergestellte Ketten, Seile und Gurte;
		"""
		html_source = P+'ketten.html'
		return txt, html_source

	def abnGel(self):
		txt = """
„abnehmbare Gelenkwelle“ 
	ein abnehmbares Bauteil zur Kraftübertragung zwischen einer Antriebs- oder 
	Zugmaschine und einer anderen Maschine, das die ersten Festlager beider 
	Maschinen verbindet. Wird die Vorrichtung zusammen mit der 
	Schutzeinrichtung in Verkehr gebracht, ist diese Kombination als ein 
	einziges Erzeugnis anzusehen;
		"""
		html_source = P+'abnGel.html'
		return txt, html_source

	def unvMasch(self):
		txt = """
„unvollständige Maschine“ 
	eine Gesamtheit, die fast eine Maschine bildet, für sich genommen aber 
	keine bestimmte Funktion erfüllen kann. Ein Antriebssystem stellt eine 
	unvollständige Maschine dar. Eine unvollständige Maschine ist nur dazu 
	bestimmt, in andere Maschinen oder in andere unvollständige Maschinen oder 
	Ausrüstungen eingebaut oder mit ihnen zusammengefügt zu werden, um 
	zusammen mit ihnen eine Maschine im Sinne dieser Richtlinie zu bilden;
		"""
		html_source = P+'unvMasch.html'
		return txt, html_source