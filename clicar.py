from time import sleep
import pyautogui
import pyperclip

# while True:
#     sleep(2)
#     print(f"\r{pyautogui.position()}",end="")
#


def paremetro():
    pyautogui.moveTo(186, 479, 0.3)
    pyautogui.click()

    pyautogui.moveTo(247, 313, 2)
    pyautogui.click()

    pyautogui.moveTo(526, 242, 0.5)
    pyautogui.click()

    pyautogui.moveTo(625, 268, 0.3)
    pyautogui.click()

    pyautogui.typewrite("transparenciaCloud")
    pyautogui.moveTo(949, 266, 0.3)
    pyautogui.click()
    pyautogui.hotkey('Shift','Home')
    pyautogui.hotkey('Backspace')
    pyperclip.copy("Enviar relatório para o Transparência Cloud")
    pyautogui.hotkey("ctrl", "v")
    pyautogui.moveTo(618, 415, 0.3)
    pyautogui.click()

    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('enter')

    pyautogui.moveTo(912, 417, 0.3)
    pyautogui.click()

    pyautogui.moveTo(919, 519, 0.3)
    pyautogui.click()

    pyautogui.moveTo(665, 679, 0.3)
    pyautogui.click()

    pyautogui.moveTo(756, 682, 0.3)
    pyautogui.click()

    pyautogui.typewrite("N")
    pyautogui.moveTo(1065, 682, 0.3)
    pyautogui.click()

    pyperclip.copy("Não")
    pyautogui.hotkey("ctrl", "v")
    pyautogui.moveTo(1295, 731, 0.3)
    pyautogui.click()

    pyautogui.moveTo(756, 712, 0.3)
    pyautogui.click()

    pyautogui.typewrite("S")
    pyautogui.moveTo(1065, 712, 0.3)
    pyautogui.click()

    pyautogui.typewrite("Sim")
    pyautogui.moveTo(1295, 767, 0.3)
    pyautogui.click()
    pyautogui.moveTo(756, 742, 0.3)
    pyautogui.click()

    pyautogui.typewrite("A")

    pyautogui.moveTo(1065, 742, 0.3)
    pyautogui.click()
    pyperclip.copy("Aguardar confirmação")
    pyautogui.hotkey("ctrl", "v")

    pyautogui.moveTo(1018, 539, 0.3)
    pyautogui.click()
    #
    pyautogui.moveTo(1004, 599, 0.3)
    pyautogui.click()

    pyautogui.moveTo(999, 870, 0.3)
    pyautogui.click()


def metadado():

    pyautogui.hotkey('esc')

    pyautogui.moveTo(345, 310, 0.3)
    pyautogui.click()

    pyautogui.moveTo(1183, 501, 2)
    pyautogui.click()

    pyautogui.moveTo(718, 489, 0.3)
    pyautogui.click()

    pyautogui.moveTo(884, 486, 0.3)
    pyautogui.click()

    pyautogui.typewrite("MTD_PUBLICAVEL_TRANSPARENCIA_CLOUD")
    pyautogui.moveTo(1039, 486, 0.3)
    pyautogui.click()

    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('enter')

    pyautogui.moveTo(1110, 583, 0.3)
    pyautogui.click()

    pyautogui.moveTo(1709, 259, 0.3)


paremetro()
sleep(8)
metadado()
