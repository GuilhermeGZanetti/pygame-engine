import pygame

from audio_manager import AudioManager

class TextRectException:
    def __init__(self, message=None):
            self.message = message

    def __str__(self):
        return self.message

def multiLineSurface(string: str, font: pygame.font.Font, rect: pygame.rect.Rect, fontColour: tuple, BGColour: tuple | None, justification=0):
        """Returns a surface containing the passed text string, reformatted
        to fit within the given rect, word-wrapping as necessary. The text
        will be anti-aliased.

        Parameters
        ----------
        string - the text you wish to render. \n begins a new line.
        font - a Font object
        rect - a rect style giving the size of the surface requested.
        fontColour - a three-byte tuple of the rgb value of the
                text color. ex (0, 0, 0) = BLACK
        BGColour - a three-byte tuple of the rgb value of the surface.
        justification - 0 (default) left-justified
                    1 horizontally centered
                    2 right-justified

        Returns
        -------
        Success - a surface object with the text rendered onto it.
        Failure - raises a TextRectException if the text won't fit onto the surface.
        """

        finalLines = []
        requestedLines = string.splitlines()
        # Create a series of lines that will fit on the provided
        # rectangle.
        for requestedLine in requestedLines:
            if font.size(requestedLine)[0] > rect.width:
                words = requestedLine.split(' ')
                # if any of our words are too long to fit, return.
                for word in words:
                    if font.size(word)[0] >= rect.width:
                        raise TextRectException("The word " + word + " is too long to fit in the rect passed.")
                # Start a new line
                accumulatedLine = ""
                for word in words:
                    testLine = accumulatedLine + word + " "
                    # Build the line while the words fit.
                    if font.size(testLine)[0] < rect.width:
                        accumulatedLine = testLine
                    else:
                        finalLines.append(accumulatedLine)
                        accumulatedLine = word + " "
                finalLines.append(accumulatedLine)
            else:
                finalLines.append(requestedLine)

        # Let's try to write the text out on the surface.
        surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        if BGColour != None:
            surface.fill(BGColour)
        accumulatedHeight = 0
        for line in finalLines:
            if accumulatedHeight + font.size(line)[1] >= rect.height:
                raise TextRectException("Once word-wrapped, the text string was too tall to fit in the rect.")
            if line != "":
                tempSurface = font.render(line, 1, fontColour)
            if justification == 0:
                surface.blit(tempSurface, (0, accumulatedHeight))
            elif justification == 1:
                surface.blit(tempSurface, ((rect.width - tempSurface.get_width()) / 2, accumulatedHeight))
            elif justification == 2:
                surface.blit(tempSurface, (rect.width - tempSurface.get_width(), accumulatedHeight))
            else:
                raise TextRectException("Invalid justification argument: " + str(justification))
            accumulatedHeight += font.size(line)[1]
        return surface


class StoryPlayer:
    def __init__(self, audio_manager: AudioManager, background_images: list[pygame.Surface], story_texts: list[str]) -> None:
        self.audio_manager = audio_manager
        self.background_images = background_images
        self.story_texts = story_texts
        self.font = pygame.font.SysFont(None, 30)

        self.current_background = 0
        self.current_text_length = 0
        self.finished_current = False

        self.text_time = 0.3

    def update(self, screen: pygame.surface.Surface) -> None:
        text_box_x = 100
        text_box_y = 2*screen.get_height()/3 - 50
        text_box_width = screen.get_width()-200
        text_box_height = screen.get_height()/3


        screen.blit(self.background_images[self.current_background], (0,0))
        text_box = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)   # per-pixel alpha
        pygame.draw.rect(text_box, (0, 0, 0, 190), (text_box_x, text_box_y, text_box_width, text_box_height), width=0, border_radius=10)
        

        # Draw text
        # Draw instruction above textbox
        text = multiLineSurface(
            "Pressione z para continuar...", 
            font=self.font, 
            rect=pygame.Rect(0, 0, 500, 28), 
            fontColour=(255, 255, 255), 
            BGColour=(0, 0, 0, 150), 
            justification=0
        )
        text_rect = text.get_rect()
        text_rect.x = text_box_x
        text_rect.y = text_box_y - 30
        text_box.blit(text, text_rect)

        # Draw story text
        text = multiLineSurface(
            self.story_texts[self.current_background][:self.current_text_length],
            font=self.font, 
            rect=pygame.Rect(0, 0, text_box_width-50, text_box_height-50), 
            fontColour=(255, 255, 255), 
            BGColour=(0, 0, 0, 0), 
            justification=0
        )
        text_rect = text.get_rect()
        text_rect.x = text_box_x + 50
        text_rect.y = text_box_y + 50
        text_box.blit(text, text_rect)


        screen.blit(text_box, (0,0))

        if not self.finished_current:
            self.current_text_length += 1
            if self.current_text_length >= len(self.story_texts[self.current_background]):
                self.finished_current = True
        

    def next(self) -> bool:
        if self.finished_current:
            self.current_background += 1
            self.current_text_length = 0
            self.finished_current = False
        else:
            self.current_text_length = len(self.story_texts[self.current_background])
            self.finished_current = True
        
        if self.current_background >= len(self.background_images):
            self.current_background = len(self.background_images)-1
            return True
        return False


