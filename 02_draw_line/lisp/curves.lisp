(load "screen.lisp")

(defstruct curve
  (x nil)
  (y nil)
  (c (make-color :r 255 :g 255 :b 255)))

(defun evaluate-curve (cv param)
  (let ((x (curve-x cv)) (y (curve-y cv)) (c (curve-c cv)))
    (values (cond ((typep x 'function) (funcall x param))
		  ((typep x 'integer) x)
		  ((typep x 'float) (round x))
		  (T nil))
	    (cond ((typep y 'function) (funcall y param))
		  ((typep y 'integer) y)
		  ((typep y 'float) (round y))
		  (T nil))
	    (cond ((typep c 'function) (funcall c param))
		  ((typep c 'color) c)
		  (T (make-color :r 255 :g 255 :b 255))))))

(defstruct curve-segment
  cv
  (start 0)
  (end 1))

(defun bezier-curve (point-list &optional (c (make-color :r 255 :g 255 :b 255)))
  (make-curve-segment 
   :cv (let ((n (- (length point-list) 1)))
	 (make-curve :c c
		     :x #'(lambda (param) (do ((i 0 (+ i 1))
					       (l point-list (cdr l))
					       (sum 0 
						    (+ sum
						       (* (car (car l))
							  (expt param i)
							  (expt (- 1 param)
								(- n i)) 
							  ()))))
					      ((> i n) sum)))