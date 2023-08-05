
from PyQt5.QtCore import Qt, QEvent, pyqtSignal as Signal, pyqtSlot as Slot
from PyQt5.QtGui import QKeySequence, QPalette, QPixmap, QMovie, QIcon
from PyQt5.QtWidgets import QMainWindow, QScrollArea, QDockWidget, QToolBar, QLabel

from .tagwidgets import TagEditor


ZOOM_FACTOR = 0
ZOOM_FITALL = 1
ZOOM_FITCUT = 2


class AutoHideMixin:
	def leaveEvent(self, ev):
		self.hide()


class AutoHideDock(QDockWidget, AutoHideMixin):
	pass
#class AutoHideToolBar(QToolBar, AutoHideMixin):
#	pass


class ImageViewer(QMainWindow):
	def __init__(self, db, *args, **kwargs):
		super(ImageViewer, self).__init__(*args, **kwargs)

		self.db = db
		self.currentIndex = -1
		self.files = []

		self._init_widgets()

	def _init_widgets(self):
		#self.toolbar = AutoHideToolBar()
		self.toolbar = QToolBar()
		self.addToolBar(self.toolbar)
		self.toolbar.hide()

		act = self.toolbar.addAction(QIcon.fromTheme('go-previous'), 'Previous')
		act.setShortcut(QKeySequence(Qt.Key_Backspace))
		act.triggered.connect(self.showPreviousFile)
		act = self.toolbar.addAction(QIcon.fromTheme('go-next'), 'Next')
		act.setShortcut(QKeySequence(Qt.Key_Space))
		act.triggered.connect(self.showNextFile)
		self.toolbar.addSeparator()

		self.toolbar.addAction(QIcon.fromTheme('zoom-original'), 'Z 1:1').triggered.connect(self.doNormalZoom)
		self.toolbar.addAction(QIcon.fromTheme('zoom-fit-best'), 'Z Fit').triggered.connect(self.doFitAllZoom)
		self.toolbar.addAction(QIcon.fromTheme('zoom-fit-best'), 'Z FitExp').triggered.connect(self.doFitCutZoom)
		self.toolbar.addAction(QIcon.fromTheme('zoom-in'), 'Z x1.5').triggered.connect(self.zoom)
		self.toolbar.addAction(QIcon.fromTheme('zoom-out'), 'Z /1.5').triggered.connect(self.unzoom)

		self.fullscreenAction = self.toolbar.addAction(QIcon.fromTheme('view-fullscreen'), 'Fullscreen')
		self.fullscreenAction.setCheckable(True)
		self.fullscreenAction.toggled.connect(self.setFullscreen)
		self.toolbar.addSeparator()

		self.toolbar.addAction('Copy tags').triggered.connect(self.copyPreviousTags)

		self.tageditor = TagEditor()
		self.tageditor.setDb(self.db)

		self.docktagger = AutoHideDock()
		self.docktagger.setWidget(self.tageditor)
		self.addDockWidget(Qt.LeftDockWidgetArea, self.docktagger)
		self.docktagger.hide()

		self.scrollview = ImageViewerCenter()
		self.scrollview.installEventFilter(self) ### !
		self.setCentralWidget(self.scrollview)

		self.scrollview.topZoneEntered.connect(self.toolbar.show)
		self.scrollview.topZoneLeft.connect(self.toolbar.hide)
		self.scrollview.leftZoneEntered.connect(self.docktagger.show)
		self.scrollview.leftZoneLeft.connect(self.docktagger.hide)

	def eventFilter(self, sview, ev):
		if ev.type() == QEvent.KeyPress:
			if ev.key() == Qt.Key_Escape:
				self.fullscreenAction.setChecked(False)
				return True
			elif ev.key() in [Qt.Key_PageUp, Qt.Key_Backspace]: # qactions
				self.showPreviousFile()
				return True
			elif ev.key() in [Qt.Key_PageDown, Qt.Key_Space]:
				self.showNextFile()
				return True
		return super(ImageViewer, self).eventFilter(sview, ev)

	@Slot()
	def doNormalZoom(self):
		self.scrollview.setZoomFactor(1.)

	@Slot()
	def doFitAllZoom(self):
		self.scrollview.setZoomMode(ZOOM_FITALL)

	@Slot()
	def doFitCutZoom(self):
		self.scrollview.setZoomMode(ZOOM_FITCUT)

	@Slot()
	def zoom(self):
		self.scrollview.multiplyZoomFactor(1.5)

	@Slot()
	def unzoom(self):
		self.scrollview.multiplyZoomFactor(1 / 1.5)

	def spawn(self, files, currentFile):
		self.files = files
		self.currentIndex = files.index(currentFile)

		self.setFile(currentFile)
		if self.isHidden():
			#~ self.setWindowState(self.windowState() | Qt.WindowMaximized)
			#~ self.show()
			self.fullscreenAction.setChecked(False)
			self.fullscreenAction.setChecked(True)
			#~ self.showMaximized()
		else:
			self.show()

	def setFile(self, file):
		self.tageditor.setFile(file)
		self.scrollview.setFile(file)
		self.setWindowTitle(file)

	@Slot()
	def copyPreviousTags(self):
		tags = self.db.find_tags_by_file(self.files[self.currentIndex - 1])
		with self.db:
			self.db.tag_file(self.files[self.currentIndex], tags)
		self.tageditor.setFile(self.files[self.currentIndex])

	def setFullscreen(self, full):
		if full:
			self.showFullScreen()
		else:
			self.showNormal()

	@Slot()
	def showPreviousFile(self):
		if self.currentIndex > 0:
			self.currentIndex -= 1
			self.setFile(self.files[self.currentIndex])

	@Slot()
	def showNextFile(self):
		if self.currentIndex < len(self.files) - 1:
			self.currentIndex += 1
			self.setFile(self.files[self.currentIndex])


class ImageViewerCenter(QScrollArea):
	topZoneEntered = Signal()
	topZoneLeft = Signal()
	leftZoneEntered = Signal()
	leftZoneLeft = Signal()

	leftMargin = 30
	topMargin = 30

	def __init__(self, *args, **kwargs):
		super(ImageViewerCenter, self).__init__(*args, **kwargs)
		self.zoomMode = ZOOM_FACTOR
		self.zoomFactor = 1
		self.moving = None

		imgWidget = QLabel()
		imgWidget.setMouseTracking(True)
		imgWidget.setAlignment(Qt.AlignCenter)
		self.setWidget(imgWidget)

		self.setAlignment(Qt.AlignCenter)
		self.setMouseTracking(True)
		self.setFrameShape(self.NoFrame)
		self.setWidgetResizable(True)

		pal = QPalette()
		pal.setColor(QPalette.Window, Qt.black)
		self.setPalette(pal)

		self.leftZone = False
		self.topZone = False

		self.file = None
		self.movie = None

	### events
	def mousePressEvent(self, ev):
		self.moving = (ev.pos().x(), ev.pos().y())
		self.movingScrolls = (self.horizontalScrollBar().value(), self.verticalScrollBar().value())

	def mouseReleaseEvent(self, ev):
		self.moving = False

	def mouseMoveEvent(self, ev):
		if self.moving:
			p = ev.pos()
			self.horizontalScrollBar().setValue(self.movingScrolls[0] - (p.x() - self.moving[0]))
			self.verticalScrollBar().setValue(self.movingScrolls[1] - (p.y() - self.moving[1]))
		else:
			newLeft = (ev.x() < self.leftMargin)
			if newLeft and not self.leftZone:
				self.leftZoneEntered.emit()
			elif self.leftZone and not newLeft:
				self.leftZoneLeft.emit()
			self.leftZone = newLeft

			newTop = (ev.y() < self.topMargin)
			if newTop and not self.topZone:
				self.topZoneEntered.emit()
			elif self.topZone and not newTop:
				self.topZoneLeft.emit()
			self.topZone = newTop

	def resizeEvent(self, ev):
		super(ImageViewerCenter, self).resizeEvent(ev)
		if self.zoomMode != ZOOM_FACTOR:
			self._rebuildZoom()

	def keyPressEvent_(self, ev):
		if ev.key() not in (Qt.Key_PageUp, Qt.Key_PageDown):
			QScrollArea.keyPressEvent(self, ev)

	def keyReleaseEvent_(self, ev):
		if ev.key() == Qt.Key_PageUp:
			self.imageviewer.prevImage_s()
		elif ev.key() == Qt.Key_PageDown:
			self.imageviewer.nextImage_s()
		else:
			QScrollArea.keyReleaseEvent(self, ev)

	### public
	def setZoomMode(self, mode):
		self.zoomMode = mode
		self._rebuildZoom()

	def setZoomFactor(self, factor):
		self.zoomFactor = factor
		self.setZoomMode(ZOOM_FACTOR)

	def multiplyZoomFactor(self, factor):
		self.setZoomFactor(self.zoomFactor * factor)

	def setFile(self, file):
		self.file = file
		if file.lower().endswith('.gif'):
			self.movie = QMovie(file)
			self.widget().setMovie(self.movie)
			self.movie.finished.connect(self.movie.start)
			self.movie.start()
		else:
			self.movie = None
			self.originalPixmap = QPixmap(file)
			self._rebuildZoom()

	###
	def _rebuildZoom(self):
		if self.movie:
			return

		if self.zoomMode == ZOOM_FACTOR:
			if self.zoomFactor == 1:
				self._setPixmap(self.originalPixmap)
			else:
				self._setPixmap(self._getScaledPixmap(self.originalPixmap.size() * self.zoomFactor))
		elif self.zoomMode == ZOOM_FITALL:
			newpix = self._getScaledPixmap(self.viewport().size())
			self._setPixmap(newpix)
			self.zoomFactor = newpix.size().width() / float(self.originalPixmap.size().width())
		elif self.zoomMode == ZOOM_FITCUT:
			newpix = self._getScaledPixmap(self.viewport().size(), Qt.KeepAspectRatioByExpanding)
			self._setPixmap(newpix)
			self.zoomFactor = newpix.size().width() / float(self.originalPixmap.size().width())

	def _getScaledPixmap(self, size, mode=Qt.KeepAspectRatio):
		return self.originalPixmap.scaled(size, mode, Qt.SmoothTransformation)

	def _setPixmap(self, pixmap):
		self.widget().setPixmap(pixmap)
