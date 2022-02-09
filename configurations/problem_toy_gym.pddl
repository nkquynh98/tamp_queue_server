(define (problem toy_gym)
    (:domain toy_gym)
    (:objects
        target_0 target_1 target_2 target_3 target_4 - location
        object_0 object_1 object_2 object_3 object_4 - object
    )
    (:init
        (agent-free)
        (target-free target_0)
        (target-free target_1)
        (target-free target_2)
        (target-free target_3)
        (target-free target_4)
    )
    (:goal 
        (and
            (at object_0 target_0)
            (at object_1 target_1)
            (at object_2 target_2)
            (at object_3 target_3)
            (at object_4 target_4)
            (agent-free)
        )
    )
)