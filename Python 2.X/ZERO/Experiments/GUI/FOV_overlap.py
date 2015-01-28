import turtle as t

def overlap(degrees):
    t.reset()
    # draw right side
    t.up()
    t.setheading(90)
    t.right(180 - degrees / 2.0)
    t.forward(100)
    t.left(90)
    t.color('red')
    t.down()
    t.fill(1)
    t.circle(100, 180)
    t.fill(0)
    # draw left side
    t.up()
    t.goto(0, 0)
    t.setheading(90)
    t.right(degrees / 2.0)
    t.forward(100)
    t.left(90)
    t.color('blue')
    t.down()
    t.fill(1)
    t.circle(100, 180)
    t.fill(0)
    # draw overlap
    t.up()
    t.goto(0, 0)
    t.fill(1)
    t.setheading(90)
    t.right(degrees / 2.0)
    t.forward(100)
    t.left(90)
    t.color('purple')
    t.down()
    t.circle(100, degrees)
    t.fill(0)
    t.up()
    t.goto(100, 100)
    t.done()