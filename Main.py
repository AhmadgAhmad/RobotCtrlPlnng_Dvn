from machine import Pin, PWM
import time

class AcebottCar:
    DATA_PIN = 5
    SHCP_PIN = 18
    STCP_PIN = 17
    EN_PIN   = 16
    PWM_PIN  = 19

    FL_FWD = 0b10000000
    FL_REV = 0b01000000

    BL_FWD = 0b00100000
    BL_REV = 0b00010000

    FR_FWD = 0b00000010
    FR_REV = 0b00000100

    BR_FWD = 0b00000001
    BR_REV = 0b00001000

    def __init__(self, freq=1000):
        self.data = Pin(self.DATA_PIN, Pin.OUT)
        self.shcp = Pin(self.SHCP_PIN, Pin.OUT)
        self.stcp = Pin(self.STCP_PIN, Pin.OUT)
        self.en   = Pin(self.EN_PIN, Pin.OUT)
        self.pwm  = PWM(Pin(self.PWM_PIN), freq=freq)

        self.data.off()
        self.shcp.off()
        self.stcp.off()

        self.en.off()   # enabled low on this board
        self.stop()

    def _shift_out(self, value):
        for i in range(8):
            bit = (value >> (7 - i)) & 1
            self.data.value(bit)
            self.shcp.off()
            self.shcp.on()
        self.shcp.off()

    def _write(self, value):
        self.stcp.off()
        self._shift_out(value)
        self.stcp.on()
        self.stcp.off()

    def set_speed(self, speed):
        speed = max(0, min(1023, speed))
        self.pwm.duty(speed)

    def raw(self, bits, speed=850, kick=1023, kick_ms=150):
        # brief kick to overcome static friction
        self._write(bits)
        if speed > 0 and kick_ms > 0:
            self.set_speed(kick)
            time.sleep_ms(kick_ms)
        self.set_speed(speed)

    def stop(self):
        self._write(0)
        self.set_speed(0)

    def forward(self, speed=850):
        self.raw(self.FL_FWD | self.BL_FWD | self.FR_FWD | self.BR_FWD, speed)

    def backward(self, speed=850):
        self.raw(self.FL_REV | self.BL_REV | self.FR_REV | self.BR_REV, speed)

    def turn_left(self, speed=850):
        self.raw(self.FL_REV | self.BL_REV | self.FR_FWD | self.BR_FWD, speed)

    def turn_right(self, speed=850):
        self.raw(self.FL_FWD | self.BL_FWD | self.FR_REV | self.BR_REV, speed)

    # These only make sense for mecanum/omni wheels
    def strafe_left(self, speed=900):
        self.raw(self.FL_REV | self.BL_FWD | self.FR_FWD | self.BR_REV, speed)

    def strafe_right(self, speed=900):
        self.raw(self.FL_FWD | self.BL_REV | self.FR_REV | self.BR_FWD, speed)

    def diag_front_left(self, speed=850):
        self.raw(self.BL_FWD | self.FR_FWD, speed)

    def diag_front_right(self, speed=850):
        self.raw(self.FL_FWD | self.BR_FWD, speed)

    def diag_back_left(self, speed=850):
        self.raw(self.FL_REV | self.BR_REV, speed)

    def diag_back_right(self, speed=850):
        self.raw(self.BL_REV | self.FR_REV, speed)

    def hw2(self, speed=850, delay=1.5):
        (self.forward)
        (self.strafe_left)
        (self.backward)
        (self.strafe_right)
        