"""
Quick quick quick, dirty dirty dirty test...
"""
import models.couch.baseCouchCollection as bcc
import models.couch.flag.flagModel as fm

import random

class test_baseCouchCollection_flags(object):
    @classmethod
    def setup_class(cls):
        for i in range(0, 100):
            title = random.choice("Normally, both your asses would be dead as fucking fried chicken, but you happen to pull this shit while I'm in a transitional period so I don't wanna kill you, I wanna help you. But I can't give you this case, it don't belong to me. Besides, I've already been through too much shit this morning over this case to hand it over to your dumb ass""".split(" "))
            description = """
    <!-- start slipsum code -->

    <h2>I can do that</h2>
    <p>Normally, both your asses would be dead as fucking fried chicken, but you happen to pull this shit while I'm in a transitional period so I don't wanna kill you, I wanna help you. But I can't give you this case, it don't belong to me. Besides, I've already been through too much shit this morning over this case to hand it over to your dumb ass. </p>

    <h2>I gotta piss</h2>
    <p>Well, the way they make shows is, they make one show. That show's called a pilot. Then they show that show to the people who make shows, and on the strength of that one show they decide if they're going to make more shows. Some pilots get picked and become television programs. Some don't, become nothing. She starred in one of the ones that became nothing. </p>

    <h2>Uuummmm, this is a tasty burger!</h2>
    <p>Your bones don't break, mine do. That's clear. Your cells react to bacteria and viruses differently than mine. You don't get sick, I do. That's also clear. But for some reason, you and I react the exact same way to water. We swallow it too fast, we choke. We get some in our lungs, we drown. However unreal it may seem, we are connected, you and I. We're on the same curve, just on opposite ends. </p>

    <h2>Hold on to your butts</h2>
    <p>Now that we know who you are, I know who I am. I'm not a mistake! It all makes sense! In a comic, you know how you can tell who the arch-villain's going to be? He's the exact opposite of the hero. And most times they're friends, like you and me! I should've known way back when... You know why, David? Because of the kids. They called me Mr Glass. </p>

    <h2>Are you ready for the truth?</h2>
    <p>Well, the way they make shows is, they make one show. That show's called a pilot. Then they show that show to the people who make shows, and on the strength of that one show they decide if they're going to make more shows. Some pilots get picked and become television programs. Some don't, become nothing. She starred in one of the ones that became nothing. </p>

    <!-- please do not remove this line -->

    <div style="display:none;">
    <a href="http://slipsum.com">lorem ipsum</a></div>

    <!-- end slipsum code -->
            """
            userid = 0
            newModel = fm.flagORM(title=title, description=description, userID=userid)
            newModel.save()

    @classmethod
    def teardown_class(cls):
        flags = fm.flagORM.all()
        for flag in flags:
            if flag["userID"] == 0:
                flag.delete()

    def test_collection(self):
        flags = fm.flagORM.all()
        collection = bcc.baseCouchCollection(fm.flagORM)
        collection.update()

        assert len(flags) == len(collection.pail)

