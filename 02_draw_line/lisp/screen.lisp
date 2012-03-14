(defstruct color
  (r 0)
  (g 0)
  (b 0))

(defun make-screen (w h &optional (bgcolor (make-color)))
  (make-array (list w h) :initial-element bgcolor))

(defun save-screen (screen filename)
  (with-open-file (fd (make-pathname :name filename) :direction :output
		                                     :if-exists :supersede)
    (format fd "P3~%~A ~A ~A~%" (array-dimension screen 0)
	                         (array-dimension screen 1)
				 256)
    (dotimes (r (array-dimension screen 1) nil)
      (dotimes (c (array-dimension screen 0) nil)
	(format fd "~A ~A ~A  " (color-r (get-pixel screen c r))
		                (color-g (get-pixel screen c r))
				(color-b (get-pixel screen c r))))
      (format fd "~%")))
  nil)

(defun draw-pixel (screen x y c)
  (when (and (typep c 'color)
	     (>= x 0)
	     (>= y 0)
	     (< x (array-dimension screen 0))
	     (< y (array-dimension screen 1)))
      (setf (aref screen x y) c))
  screen)



(defun get-pixel (screen x y)
  (if (and (>= x 0)
	   (>= y 0)
	   (< x (array-dimension screen 0))
	   (< y (array-dimension screen 1)))
      (aref screen x y)
      (make-color)))

(defun (setf get-pixel) (val screen x y)
  (draw-pixel screen x y val))