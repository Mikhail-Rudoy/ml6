(load "screen.lisp")
(load "io.lisp")

(defparameter screen (make-screen 600 600))

(message 'drawing "...")
(dotimes (x 600 x)
  (dotimes (y 600 y)
    (setf (get-pixel screen x y) (make-color :r (random 256)
					     :g (random 256)
					     :b (random 256)))))
(message 'drawn "")

(message 'saving "...")
(save-screen screen "pic.ppm")
(message 'saved)