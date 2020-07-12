(define (problem ControlCentralLight)
(:domain CentralLight)
 (:objects led1 GUI1 user1 Alexa1)
 (:init (led led1) (GUI GUI1) (user user1)(Alexa Alexa1))
 (:goal (and (ON led1) (Display GUI1)))
)
 
