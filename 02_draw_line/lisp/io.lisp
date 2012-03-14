(defun message (&rest args)
  (dolist (obj args)
    (format t "~A~%" obj))
  nil)