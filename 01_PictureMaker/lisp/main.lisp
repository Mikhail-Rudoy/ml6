(load "screen.lisp")

(defparameter screen (make-screen 600 600))

(dotimes (x 600 x)
  (dotimes (y 600 y)
    (draw-pixel screen x y (make-color :r (random 256)
				       :g (random 256)
				       :b (random 256)))))

(format t "~A~%" 'saving)
(save-screen screen "pic.ppm")
(format t "~A" 'saved)