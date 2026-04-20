from machine import Pin, PWM
import time

# ── ACEBOTT QA052 Car Shield Pins ─────────────────────────────────────
SHCP = Pin(18, Pin.OUT)   # Shift register clock
EN   = Pin(16, Pin.OUT)   # Enable
DATA = Pin(5,  Pin.OUT)   # Serial data
STCP = Pin(17, Pin.OUT)   # Latch

# PWM pins — one per motor
pwm1 = PWM(Pin(19), freq=1000)
pwm2 = PWM(Pin(21), freq=1000)
pwm3 = PWM(Pin(22), freq=1000)
pwm4 = PWM(Pin(23), freq=1000)

# ── Direction bits for each motor ─────────────────────────────────────
M1_F = 0b10000000;  M1_B = 0b01000000
M2_F = 0b00100000;  M2_B = 0b00010000
M3_F = 0b00001000;  M3_B = 0b00000100
M4_F = 0b00000010;  M4_B = 0b00000001

# ── Shift register helper ──────────────────────────────────────────────
def shift_out(data):
    EN.value(0)
    STCP.value(0)
    for i in range(7, -1, -1):
        SHCP.value(0)
        DATA.value((data >> i) & 1)
        SHCP.value(1)
    STCP.value(1)

# ── Speed helper ───────────────────────────────────────────────────────
# speed: 0 (stopped) to 100 (full speed)
# Internally maps 0-100 → 0-1023 (ESP32 PWM range)
def set_speed(speed):
    duty = int(speed * 1023 / 100)   # convert % to duty cycle
    duty = max(0, min(1023, duty))   # clamp to safe range
    pwm1.duty(duty)
    pwm2.duty(duty)
    pwm3.duty(duty)
    pwm4.duty(duty)

# ── Movement functions (now accept a speed %) ──────────────────────────
def forward(speed=60):
    shift_out(M1_F | M2_F | M3_F | M4_F)
    set_speed(speed)

def backward(speed=60):
    shift_out(M1_B | M2_B | M3_B | M4_B)
    set_speed(speed)

def turn_left(speed=50):
    shift_out(M1_B | M2_F | M3_B | M4_F)
    set_speed(speed)

def turn_right(speed=50):
    shift_out(M1_F | M2_B | M3_F | M4_B)
    set_speed(speed)

def stop():
    shift_out(0b00000000)
    set_speed(0)

# ══════════════════════════════════════════════════════════════════════
# EXPERIMENT 1: Compare slow vs fast
# Can you feel the difference? Watch how the wheels behave!
# ══════════════════════════════════════════════════════════════════════
print("--- Experiment 1: Slow vs Fast ---")

print("Slow (30%)");  forward(speed=30);  time.sleep(2)
stop();               time.sleep(1)

print("Medium (60%)"); forward(speed=60); time.sleep(2)
stop();               time.sleep(1)

print("Fast (90%)");  forward(speed=90);  time.sleep(2)
stop();               time.sleep(1)

# ══════════════════════════════════════════════════════════════════════
# EXPERIMENT 2: Gradual acceleration (ramp up)
# Speed goes from 20% to 100% smoothly — like a real car!
# ══════════════════════════════════════════════════════════════════════
print("--- Experiment 2: Ramp Up ---")
shift_out(M1_F | M2_F | M3_F | M4_F)   # set direction: forward
for speed in range(20, 101, 5):         # 20 → 100, step by 5
    print("Speed:", speed, "%")
    set_speed(speed)
    time.sleep(0.2)
stop()
time.sleep(1)

# ══════════════════════════════════════════════════════════════════════
# EXPERIMENT 3: Drive a square at controlled speed
# Each side: forward for 1.5s, then turn 90° for 0.6s
# CHALLENGE: Tune the time values so it makes a proper square!
# ══════════════════════════════════════════════════════════════════════
print("--- Experiment 3: Square Path ---")
for side in range(4):
    print("Side", side + 1)
    forward(speed=50);    time.sleep(1.5)   # adjust time to tune distance
    stop();               time.sleep(0.2)
    turn_right(speed=50); time.sleep(0.6)   # adjust time to tune turn angle
    stop();               time.sleep(0.2)

print("Done! Did it draw a square?")
