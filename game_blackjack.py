"""
Blackjack Card Game - Modern GUI Version
Player vs Dealer with chip betting system, card visuals, and smooth animations
"""

import customtkinter as ctk
import random
from tkinter import messagebox


# Set appearance mode and color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class Card:
    """Represents a playing card"""

    SUITS = ['\u2660', '\u2665', '\u2666', '\u2663']  # Spades, Hearts, Diamonds, Clubs
    SUIT_NAMES = {'\u2660': 'Spades', '\u2665': 'Hearts', '\u2666': 'Diamonds', '\u2663': 'Clubs'}
    RANK_NAMES = {
        'A': 'Ace', '2': '2', '3': '3', '4': '4', '5': '5',
        '6': '6', '7': '7', '8': '8', '9': '9', '10': '10',
        'J': 'Jack', 'Q': 'Queen', 'K': 'King'
    }

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.face_up = True

    def value(self):
        """Return card value for Blackjack"""
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)

    def is_red(self):
        return self.suit in ['\u2665', '\u2666']

    def __str__(self):
        if self.face_up:
            return f"{self.rank}{self.suit}"
        return "??"


class Deck:
    """Standard 52-card deck"""

    def __init__(self):
        self.cards = []
        self.reset()

    def reset(self):
        """Create and shuffle a new deck"""
        self.cards = []
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        for suit in Card.SUITS:
            for rank in ranks:
                self.cards.append(Card(rank, suit))
        random.shuffle(self.cards)

    def deal(self):
        """Deal one card"""
        if len(self.cards) < 10:
            self.reset()
        return self.cards.pop()


class Hand:
    """Represents a hand of cards"""

    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def score(self):
        """Calculate hand score, handling Aces properly"""
        total = 0
        aces = 0
        for card in self.cards:
            if card.face_up:
                total += card.value()
                if card.rank == 'A':
                    aces += 1

        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

    def is_blackjack(self):
        return len(self.cards) == 2 and self.score() == 21

    def is_busted(self):
        return self.score() > 21


class CardWidget(ctk.CTkFrame):
    """Visual representation of a card in the GUI"""

    def __init__(self, parent, card=None, width=90, height=130):
        super().__init__(parent, width=width, height=height, corner_radius=10)
        self.card_width = width
        self.card_height = height
        self.card = card
        self.pack_propagate(False)

        self._build_ui()
        if card:
            self.update_card(card)

    def _build_ui(self):
        """Build the card visual elements"""
        self.configure(fg_color="#1a1a2e", border_width=2, border_color="#3d3d5c")

        self.top_label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white", anchor="nw"
        )
        self.top_label.place(x=8, y=5)

        self.center_label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=40),
            text_color="white", anchor="center"
        )
        self.center_label.place(relx=0.5, rely=0.5, anchor="center")

        self.bottom_label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white", anchor="se"
        )
        self.bottom_label.place(x=8, rely=1.0, y=-5, anchor="sw")

    def update_card(self, card):
        """Update the card display"""
        self.card = card
        if card.face_up:
            color = "#e74c3c" if card.is_red() else "#ecf0f1"
            display = f"{card.rank}{card.suit}"
            self.top_label.configure(text=display, text_color=color)
            self.center_label.configure(text=card.suit, text_color=color)
            self.bottom_label.configure(text=display, text_color=color)
            self.configure(fg_color="#fefefe", border_color="#cccccc")
        else:
            self.top_label.configure(text="", text_color="#7f8c8d")
            self.center_label.configure(text="\u2766", text_color="#3498db")  # Decorative back
            self.bottom_label.configure(text="", text_color="#7f8c8d")
            self.configure(fg_color="#16213e", border_color="#0f3460")


class BlackjackGame(ctk.CTk):
    """Blackjack Game Application"""

    def __init__(self):
        super().__init__()

        self.title("\u2660 Blackjack \u2660")
        self.geometry("900x750")
        self.resizable(True, True)
        self.minsize(800, 700)

        # Game state
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.chips = 1000
        self.current_bet = 0
        self.game_in_progress = False
        self.player_stood = False
        self.can_double = False
        self.wins = 0
        self.losses = 0
        self.pushes = 0

        # Animation tracking
        self.animating = False

        self.setup_ui()
        self.new_hand()

    def setup_ui(self):
        """Setup the User Interface"""

        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # ========== HEADER ==========
        self.header_frame = ctk.CTkFrame(self.main_frame)
        self.header_frame.pack(fill="x", pady=(0, 10))

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="\u2660 BLACKJACK \u2660",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.title_label.pack(pady=8)

        # ========== STATS BAR ==========
        self.stats_frame = ctk.CTkFrame(self.main_frame)
        self.stats_frame.pack(fill="x", pady=(0, 10))

        self.chips_label = ctk.CTkLabel(
            self.stats_frame,
            text=f"\U0001FA99 Chips: {self.chips}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#f1c40f"
        )
        self.chips_label.pack(side="left", padx=15, pady=8)

        self.bet_label = ctk.CTkLabel(
            self.stats_frame,
            text=f"\U0001F4B0 Bet: 0",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#2ecc71"
        )
        self.bet_label.pack(side="left", padx=15, pady=8)

        self.record_label = ctk.CTkLabel(
            self.stats_frame,
            text=f"W: {self.wins}  L: {self.losses}  P: {self.pushes}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#bdc3c7"
        )
        self.record_label.pack(side="right", padx=15, pady=8)

        # ========== DEALER SECTION ==========
        self.dealer_frame = ctk.CTkFrame(self.main_frame, fg_color="#1e1e3a", corner_radius=12)
        self.dealer_frame.pack(fill="x", pady=(0, 8), padx=5)

        self.dealer_label = ctk.CTkLabel(
            self.dealer_frame,
            text="Dealer's Hand",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#e0e0e0"
        )
        self.dealer_label.pack(pady=(10, 5))

        self.dealer_score_label = ctk.CTkLabel(
            self.dealer_frame,
            text="Score: 0",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#f39c12"
        )
        self.dealer_score_label.pack(pady=(0, 5))

        self.dealer_cards_frame = ctk.CTkFrame(self.dealer_frame, fg_color="transparent")
        self.dealer_cards_frame.pack(fill="x", expand=True, padx=10, pady=5)
        self.dealer_card_widgets = []

        # ========== STATUS MESSAGE ==========
        self.status_frame = ctk.CTkFrame(self.main_frame)
        self.status_frame.pack(fill="x", pady=8)

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Place your bet to begin",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.status_label.pack(pady=5)

        # ========== PLAYER SECTION ==========
        self.player_frame = ctk.CTkFrame(self.main_frame, fg_color="#1e1e3a", corner_radius=12)
        self.player_frame.pack(fill="x", pady=(8, 0), padx=5)

        self.player_score_label = ctk.CTkLabel(
            self.player_frame,
            text="Score: 0",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#f39c12"
        )
        self.player_score_label.pack(pady=(5, 0))

        self.player_label = ctk.CTkLabel(
            self.player_frame,
            text="Your Hand",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#e0e0e0"
        )
        self.player_label.pack(pady=(5, 5))

        self.player_cards_frame = ctk.CTkFrame(self.player_frame, fg_color="transparent")
        self.player_cards_frame.pack(fill="x", expand=True, padx=10, pady=5)
        self.player_card_widgets = []

        # ========== BETTING SECTION ==========
        self.bet_frame = ctk.CTkFrame(self.main_frame)
        self.bet_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            self.bet_frame,
            text="Bet Amount:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=(15, 5), pady=10)

        self.bet_var = ctk.StringVar(value="50")
        self.bet_entry = ctk.CTkEntry(
            self.bet_frame,
            textvariable=self.bet_var,
            width=100,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=8
        )
        self.bet_entry.pack(side="left", padx=5, pady=10)

        # Quick bet buttons
        for amount in [25, 50, 100, 250, 500]:
            btn = ctk.CTkButton(
                self.bet_frame,
                text=f"{amount}",
                width=60,
                height=35,
                corner_radius=8,
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color="#34495e",
                hover_color="#4a6785",
                command=lambda a=amount: self.set_bet(a)
            )
            btn.pack(side="left", padx=3, pady=10)

        # ========== ACTION BUTTONS ==========
        self.actions_frame = ctk.CTkFrame(self.main_frame)
        self.actions_frame.pack(fill="x", pady=10)

        self.deal_btn = ctk.CTkButton(
            self.actions_frame,
            text="\U0001F0CF  Deal",
            command=self.deal_cards,
            font=ctk.CTkFont(size=18, weight="bold"),
            height=50,
            corner_radius=12,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        self.deal_btn.pack(side="left", padx=10, pady=5, expand=True, fill="x")

        self.hit_btn = ctk.CTkButton(
            self.actions_frame,
            text="\u270B  Hit",
            command=self.hit,
            font=ctk.CTkFont(size=18, weight="bold"),
            height=50,
            corner_radius=12,
            fg_color="#3498db",
            hover_color="#2980b9",
            state="disabled"
        )
        self.hit_btn.pack(side="left", padx=10, pady=5, expand=True, fill="x")

        self.stand_btn = ctk.CTkButton(
            self.actions_frame,
            text="\u270B  Stand",
            command=self.stand,
            font=ctk.CTkFont(size=18, weight="bold"),
            height=50,
            corner_radius=12,
            fg_color="#e67e22",
            hover_color="#d35400",
            state="disabled"
        )
        self.stand_btn.pack(side="left", padx=10, pady=5, expand=True, fill="x")

        self.double_btn = ctk.CTkButton(
            self.actions_frame,
            text="\U0001F4B0  Double Down",
            command=self.double_down,
            font=ctk.CTkFont(size=18, weight="bold"),
            height=50,
            corner_radius=12,
            fg_color="#9b59b6",
            hover_color="#8e44ad",
            state="disabled"
        )
        self.double_btn.pack(side="left", padx=10, pady=5, expand=True, fill="x")

    def set_bet(self, amount):
        """Set bet amount quickly"""
        self.bet_var.set(str(min(amount, self.chips)))

    def new_hand(self):
        """Prepare for a new hand"""
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.player_stood = False
        self.can_double = False
        self.game_in_progress = False

        # Clear card widgets
        for widget in self.dealer_card_widgets:
            widget.destroy()
        self.dealer_card_widgets = []

        for widget in self.player_card_widgets:
            widget.destroy()
        self.player_card_widgets = []

        self.update_display()

    def get_bet_amount(self):
        """Get and validate bet amount"""
        try:
            bet = int(self.bet_var.get())
            if bet <= 0:
                messagebox.showwarning("Invalid Bet", "Bet must be greater than 0")
                return 0
            if bet > self.chips:
                messagebox.showwarning("Insufficient Chips", f"You only have {self.chips} chips!")
                return 0
            return bet
        except ValueError:
            messagebox.showwarning("Invalid Bet", "Please enter a valid number")
            return 0

    def deal_cards(self):
        """Start a new hand"""
        if self.game_in_progress:
            return

        bet = self.get_bet_amount()
        if bet == 0:
            return

        self.current_bet = bet
        self.chips -= bet
        self.game_in_progress = True

        # Deal initial cards
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())

        # Enable action buttons
        self.hit_btn.configure(state="normal")
        self.stand_btn.configure(state="normal")

        # Can double if enough chips
        self.can_double = self.chips >= self.current_bet
        self.double_btn.configure(state="normal" if self.can_double else "disabled")
        self.deal_btn.configure(state="disabled")

        # Check for blackjacks
        if self.player_hand.is_blackjack() or self.dealer_hand.is_blackjack():
            self.resolve_blackjacks()
            return

        self.update_display()
        self.set_status("Your turn: Hit, Stand, or Double Down", "#3498db")

    def hit(self):
        """Player requests another card"""
        if not self.game_in_progress or self.player_stood:
            return

        self.player_hand.add_card(self.deck.deal())
        self.can_double = False
        self.double_btn.configure(state="disabled")

        self.update_display()

        if self.player_hand.is_busted():
            self.end_round("bust")
        elif self.player_hand.score() == 21:
            self.stand()

    def stand(self):
        """Player stands"""
        if not self.game_in_progress or self.player_stood:
            return

        self.player_stood = True
        self.hit_btn.configure(state="disabled")
        self.stand_btn.configure(state="disabled")
        self.double_btn.configure(state="disabled")

        self.set_status("Dealer's turn...", "#f39c12")
        self.after(800, self.dealer_play)

    def double_down(self):
        """Double the bet and take exactly one more card"""
        if not self.game_in_progress or not self.can_double or len(self.player_hand.cards) != 2:
            return

        self.chips -= self.current_bet
        self.current_bet *= 2
        self.update_display()

        self.player_hand.add_card(self.deck.deal())
        self.update_display()

        if self.player_hand.is_busted():
            self.end_round("bust")
        else:
            self.stand()

    def dealer_play(self):
        """Dealer plays according to rules"""
        # Reveal dealer's hidden card
        self.dealer_hand.cards[1].face_up = True

        if self.dealer_hand.is_blackjack():
            self.update_display()
            self.end_round("dealer_blackjack")
            return

        self.after(600, self._dealer_draw)

    def _dealer_draw(self):
        """Dealer draws cards"""
        while self.dealer_hand.score() < 17:
            self.dealer_hand.add_card(self.deck.deal())

        self.update_display()
        self.after(500, lambda: self.resolve_dealer_hand())

    def resolve_dealer_hand(self):
        """Compare hands and determine winner"""
        if self.dealer_hand.is_busted():
            self.end_round("dealer_bust")
        elif self.dealer_hand.score() > self.player_hand.score():
            self.end_round("dealer_wins")
        elif self.player_hand.score() > self.dealer_hand.score():
            self.end_round("player_wins")
        else:
            self.end_round("push")

    def resolve_blackjacks(self):
        """Handle when player or dealer has blackjack"""
        # Reveal dealer's hand
        self.dealer_hand.cards[1].face_up = True

        if self.player_hand.is_blackjack() and self.dealer_hand.is_blackjack():
            self.end_round("both_blackjack")
        elif self.player_hand.is_blackjack():
            self.end_round("player_blackjack")
        else:
            self.end_round("dealer_blackjack")

    def end_round(self, result):
        """End the round and determine payout"""
        self.game_in_progress = False
        self.hit_btn.configure(state="disabled")
        self.stand_btn.configure(state="disabled")
        self.double_btn.configure(state="disabled")

        message = ""
        color = "#ecf0f1"
        payout = 0

        if result == "bust":
            message = f"\U0001F4A5 BUST! You lose {self.current_bet} chips"
            color = "#e74c3c"
            self.losses += 1
        elif result == "dealer_bust":
            payout = self.current_bet * 2
            self.chips += payout
            message = f"\U0001F389 Dealer BUSTS! You win {self.current_bet} chips!"
            color = "#2ecc71"
            self.wins += 1
        elif result == "player_wins":
            payout = self.current_bet * 2
            self.chips += payout
            message = f"\U0001F389 You Win! +{self.current_bet} chips"
            color = "#2ecc71"
            self.wins += 1
        elif result == "dealer_wins":
            message = f"\U0001F614 Dealer Wins. -{self.current_bet} chips"
            color = "#e74c3c"
            self.losses += 1
        elif result == "push":
            self.chips += self.current_bet
            message = "\U0001F91D PUSH! Bet returned"
            color = "#f39c12"
            self.pushes += 1
        elif result == "player_blackjack":
            payout = int(self.current_bet * 2.5)  # 3:2 payout
            self.chips += payout
            message = f"\U0001F0CF BLACKJACK! +{int(self.current_bet * 1.5)} chips"
            color = "#f1c40f"
            self.wins += 1
        elif result == "dealer_blackjack":
            message = f"\U0001F0CF Dealer Blackjack! -{self.current_bet} chips"
            color = "#e74c3c"
            self.losses += 1
        elif result == "both_blackjack":
            self.chips += self.current_bet
            message = "\U0001F91D Both Blackjack! PUSH"
            color = "#f39c12"
            self.pushes += 1

        self.set_status(message, color)
        self.update_display()

        # Check if player is out of chips
        if self.chips <= 0:
            self.after(1500, self.out_of_chips)

    def out_of_chips(self):
        """Handle when player runs out of chips"""
        if messagebox.askyesno("Out of Chips", "You're out of chips! Start a new game with 1000 chips?"):
            self.chips = 1000
            self.wins = 0
            self.losses = 0
            self.pushes = 0
            self.current_bet = 0
            self.new_hand()
            self.update_display()
        else:
            self.quit()

    def update_display(self):
        """Update all UI elements"""
        self.update_dealer_hand()
        self.update_player_hand()

        # Update labels
        self.chips_label.configure(text=f"\U0001FA99 Chips: {self.chips}")
        self.bet_label.configure(text=f"\U0001F4B0 Bet: {self.current_bet}")
        self.record_label.configure(text=f"W: {self.wins}  L: {self.losses}  P: {self.pushes}")

        # Update scores
        if self.dealer_hand.cards:
            if self.player_stood or not self.game_in_progress:
                dealer_score = self.dealer_hand.score()
            else:
                dealer_score = self.dealer_hand.cards[0].value() if self.dealer_hand.cards[0].face_up else 0
            self.dealer_score_label.configure(text=f"Score: {dealer_score}")

        if self.player_hand.cards:
            self.player_score_label.configure(text=f"Score: {self.player_hand.score()}")

    def update_dealer_hand(self):
        """Update dealer card display"""
        for widget in self.dealer_card_widgets:
            widget.destroy()
        self.dealer_card_widgets = []

        for card in self.dealer_hand.cards:
            card_widget = CardWidget(self.dealer_cards_frame, card)
            card_widget.pack(side="left", padx=5, pady=5)
            self.dealer_card_widgets.append(card_widget)

    def update_player_hand(self):
        """Update player card display"""
        for widget in self.player_card_widgets:
            widget.destroy()
        self.player_card_widgets = []

        for card in self.player_hand.cards:
            card_widget = CardWidget(self.player_cards_frame, card)
            card_widget.pack(side="left", padx=5, pady=5)
            self.player_card_widgets.append(card_widget)

    def set_status(self, text, color="#ecf0f1"):
        """Update status message"""
        self.status_label.configure(text=text, text_color=color)


if __name__ == "__main__":
    app = BlackjackGame()
    app.mainloop()
