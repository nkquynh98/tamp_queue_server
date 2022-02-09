(define (domain toy_gym)
  (:requirements :typing)
  (:types location object)
  (:constants
    target_0 target_1 target_2 target_3 target_4 - location
    object_0 object_1 object_2 object_3 object_4 - object
  )
  (:predicates
    (at ?x - object ?l - location)
    (target-free ?l)
    (agent-free)
    (agent-carry ?x - object)
  )

  (:durative-action movetopick
      :parameters (?x - object)
      :duration (= ?duration 25)
      :precondition (and (at start (agent-free))) 
      :effect (and (at end (not (agent-free))) (at end (agent-carry ?x)))
  )

  (:durative-action movetoplace
      :parameters (?x - object ?l - location)
      :duration (= ?duration 25)
      :precondition (and (at start (agent-carry ?x))(at start (target-free ?l)))  
      :effect (and (at end (not (agent-carry ?x))) (at end (at ?x ?l)) (at end (agent-free))(at end (not (target-free ?l))))
  )
)