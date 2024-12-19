import pygame
import sys

heigth, width = 700, 1000
pygame.init()
screen = pygame.display.set_mode((width, heigth))
pygame.display.set_caption("Spirit")

colors = {
    "black": (0, 0, 0),
    "white": (230, 230, 230),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255)
}
address_list = ["0x123456", "0x987654", "0x876554"]
heap_block_states = [colors["black"]] * 3  
heap_addresses = [""] * 3  
last_allocated_index = -1  
arrow_position = None 
malicious_address = "0x666777"  # the malicious address

def create_bin():
    x = 0
    text = pygame.font.Font(None, 36)
    text_surface = text.render("Fast bin", True, colors["black"])
    screen.blit(text_surface, (380, 110))
    pygame.draw.rect(screen, colors["black"], (350, 100, 200, 300), 2)
    for i in range(4):
        pygame.draw.rect(screen, colors["black"], (350, 100 + x, 200, 40), 2)
        x += 300 / 4
    create_bin_address()

def create_bin_address():
    y = 230
    for address in reversed(address_list):  #reverse the list to show the address from top to bottom
        text = pygame.font.Font(None, 36)
        text_surface = text.render(address, True, colors["black"])
        screen.blit(text_surface, (360, y))
        y -= 300 / 8

def the_malloc():
    global last_allocated_index, arrow_position
    if address_list:
        #pop the first address from the bin
        address = address_list.pop(0)
        
        #loop to check if there is a free block in the heap
        for i in range(len(heap_block_states)):
            if heap_block_states[i] in (colors["black"], colors["green"]):
                heap_block_states[i] = colors["red"]
                #save the address in the heap
                heap_addresses[i] = address  
                #update the last allocated index
                last_allocated_index = i  
                #update the arrow position
                arrow_position = (70, 220 + last_allocated_index * 100)  
                break
            pygame.display.update()        
                    
            

def the_free():
    fake_bloke_position=(735, 190)
    global last_allocated_index, arrow_position
    #check if the arrow is in the fake block
    if arrow_position == fake_bloke_position:
        #insert the malicious address to the bin
        address_list.insert(0, malicious_address) 
        arrow_position = None  
    elif last_allocated_index != -1:
        #insert the address to the bin
        address_list.insert(0, heap_addresses[last_allocated_index])
        
       #update the heap block states and addresses
        heap_block_states[last_allocated_index] = colors["green"]
        heap_addresses[last_allocated_index] = ""
        
        #update the last allocated index
        last_allocated_index = -1
        for i in range(len(heap_block_states) - 1, -1, -1):
            if heap_block_states[i] == colors["red"]:
                last_allocated_index = i
                arrow_position = (70, 220 + last_allocated_index * 100) 
                break


def move_the_address():
    global arrow_position
    if arrow_position:
        #the start position of the arrow
        start_x, start_y = arrow_position
        #the target position of the arrow
        target_x = 735
        target_y = 190
        steps = 50  
        #loop to move the arrow from the start position to the target position
        for i in range(steps):
            
            current_x = start_x + (target_x - start_x) * i / steps
            current_y = start_y + (target_y - start_y) * i / steps

            #update the screen
            screen.fill(colors["white"])
            create_bin()
            create_heap()
            create_fake_block()
            the_attack()
            free_button(colors["green"])
            malloc_button(colors["red"])

            #draw the arrow
            pygame.draw.polygon(screen, colors["blue"], [
                (current_x, current_y),
                (current_x + 20, current_y - 20),
                (current_x - 20, current_y - 20)
            ])

            pygame.display.update()
            pygame.time.delay(20)  

        #update the arrow position
        arrow_position = (target_x, target_y)

#function to create the heap
def create_heap():
    x = 0
    text=  pygame.font.Font(None, 50)
    text_surface = text.render(" The Heap", True, colors["black"])
    screen.blit(text_surface, (50, 50))
    pygame.draw.rect(screen, colors["black"], (250, 120, 80, 5))
    pygame.draw.polygon(screen, colors["black"], [(340, 122), (320, 115), (320, 129)])
    pygame.draw.rect(screen, colors["black"], (50, 100, 200, 400), 2)
    text = pygame.font.Font(None, 36)
    text_surface = text.render("bins", True, colors["black"])
    screen.blit(text_surface, (100, 110 + x))

    #loop to create the heap blocks
    for i in range(3):
        pygame.draw.rect(screen, heap_block_states[i], (50, 200 + x, 200, 100), 4)
        pygame.draw.rect(screen, colors["black"], (50, 200 + x, 200, 40), 2)
        text = pygame.font.Font(None, 36)
        text_surface = text.render("meta data", True, colors["black"])
        screen.blit(text_surface, (100, 210 + x))

        #check if the address is in the heap
        if heap_addresses[i]:
            address_surface = text.render(heap_addresses[i], True, colors["black"])
            screen.blit(address_surface, (60, 250 + x))
            if heap_addresses[i] == malicious_address:
                malicious_text = pygame.font.Font(None, 20)
                malicious_surface = malicious_text.render("MALICIOUS DATA!!!", True, colors["red"]) 
                screen.blit(malicious_surface, (60, 280 + x))

        x += 400 / 4

    #draw the arrow
    if arrow_position:
        pygame.draw.polygon(screen, colors["blue"], [
            (arrow_position[0], arrow_position[1]),
            (arrow_position[0] + 20, arrow_position[1] - 20),
            (arrow_position[0] - 20, arrow_position[1] - 20)
        ])

#function to create the fake block
def create_fake_block():
    pygame.draw.rect(screen, colors["black"], (600, 200, 200, 100), 4)
    pygame.draw.rect(screen, colors["black"], (600, 200, 200, 40), 2)
    text = pygame.font.Font(None, 36)
    text_surface = text.render("meta data", True, colors["black"])
    screen.blit(text_surface, (620, 210))
    text_surface = text.render("Malicious data", True, colors["red"])
    screen.blit(text_surface, (610, 250))
    text = pygame.font.Font(None, 30)
    block= text.render("The malicious block", True, colors["black"])
    screen.blit(block, (610, 125))
    the_address=text.render("The address is:", True, colors["black"])
    screen.blit(the_address, (610, 150))
    address = text.render(malicious_address, True, colors["black"])
    screen.blit(address, (610, 175))

#function to create the free buttons
def free_button(color):
    pygame.draw.rect(screen, color, (520, 600, 200, 50), border_radius=10)
    text = pygame.font.Font(None, 50)
    text_surface = text.render("Free", True, colors["black"])
    screen.blit(text_surface, (530, 610))

#function to create the malloc button
def malloc_button(color):
    pygame.draw.rect(screen, color, (300, 600, 200, 50), border_radius=10)
    text = pygame.font.Font(None, 50)
    text_surface = text.render("Malloc", True, colors["black"])
    screen.blit(text_surface, (310, 610))

#function to create the attack button
def the_attack():
    pygame.draw.rect(screen, colors["black"], (730, 600, 200, 50), border_radius=10)
    text = pygame.font.Font(None, 30)
    text_surface = text.render("Trigger Overflow", True, colors["white"])
    screen.blit(text_surface, (740, 610))

  
def main():
    
    while True:
        screen.fill(colors["white"])
        text = pygame.font.Font(None, 35)
        text_surface = text.render("House Of Spirit", True, colors["black"])
        screen.blit(text_surface, (400, 10))
        create_bin()
        create_heap()
        create_fake_block()
        the_attack()
        free_button(colors["green"])
        malloc_button(colors["red"])
        


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 520 <= event.pos[0] <= 720 and 520 <= event.pos[1] <= 720:
                    the_free()
                elif 300 <= event.pos[0] <= 500 and 600 <= event.pos[1] <= 650:
                    the_malloc()
                elif 730 <= event.pos[0] <= 920 and 600 <= event.pos[1] <= 650:
                    move_the_address()
              

        pygame.display.update()
        pygame.time.delay(30)

if __name__ == "__main__":
    main()