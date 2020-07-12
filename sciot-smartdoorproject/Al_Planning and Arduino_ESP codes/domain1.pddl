(define (domain CentralLight)
    (:requirements 
        :strips 
        :typing
        :negative-preconditions
    )
    
    (:predicates
      (led ?l)
      (ON ?l)
      (Alexa ?a)
      (Input ?a)
      (GUI ?g)
      (Display ?g)
	  (user ?k)
    )
    
    (:action Led-ON
      :parameters (?l ?a)
      :precondition (and (led ?l) (not(ON ?l)) (Input ?a))
      :effect (ON ?l)
    )
    
    
    (:action Led-OFF
      :parameters (?l ?a)
      :precondition (and (led ?l) (ON ?l) (not(Input ?a)))
      :effect (not (ON ?l))
    )
    
    
    (:action Alexa-ON-Input
      :parameters (?a ?k ?l)
      :precondition (and (user ?k) (Alexa ?a) (not(Input ?a)))
      :effect (Input ?a)
    )
    
    
    (:action Alexa-OFF-Input
      :parameters (?a ?k ?l)
      :precondition (and (user ?k) (Alexa ?a) (Input ?a))
      :effect (not(Input ?a))
    )
    
    (:action GUI-ON-Display
      :parameters (?g ?l)
      :precondition (and (not(Display ?g)) (ON ?l))
      :effect (Display ?g)
    )
    
    (:action GUI-OFF-Display
      :parameters (?g ?l)
      :precondition (and (Display ?g) (not(ON ?l)))
      :effect (not (Display ?g))
    )
)             

 
