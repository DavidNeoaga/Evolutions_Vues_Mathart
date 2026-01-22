from manim import *
import numpy as np

class EvolutionVues(Scene):
    def construct(self):
        # Infos de base
        total_days = 32
        final_views = 536
        
        # Axes
        axes = Axes(
            x_range=[0, total_days, 5],
            y_range=[0, 600, 100],
            x_length=10,
            y_length=6,
            axis_config={"color": WHITE, "include_tip": False, "include_numbers": False}, 
        ).center()

        # Texte Axes
        y_labels = VGroup()
        for y_val in range(0, 601, 100):
            label = Text(str(y_val), font_size=16).next_to(axes.c2p(0, y_val), LEFT)
            y_labels.add(label)
            
        date_start = Text("10 Déc", font_size=16).next_to(axes.c2p(0, 0), DOWN)
        date_mid = Text("25 Déc", font_size=16).next_to(axes.c2p(15, 0), DOWN)
        date_end = Text("Auj.", font_size=16).next_to(axes.c2p(total_days, 0), DOWN)
        y_title = Text("Vues", font_size=20).next_to(axes.y_axis, UP)

        # 3. La courbe
        def curve_func(x):
            # Formule de base
            val_raw = 1 / (1 + np.exp(-0.2 * (x - total_days/2)))
            # Calcul de la valeur max atteinte théorique à la fin (pour normaliser)
            max_reached = 1 / (1 + np.exp(-0.2 * (total_days - total_days/2)))
            
            # On divise par le max atteint pour être sûr d'arriver à 100% (soit 1.0)
            normalized_val = val_raw / max_reached
            
            return final_views * normalized_val

        graph = axes.plot(curve_func, color=RED, stroke_width=4)

        # 4. Le point et le compteur
        dot = Dot(color=RED).scale(1.2)
        dot.move_to(axes.i2gp(0, graph))
        
        tracker = ValueTracker(0)
        number_display = Text("0", font_size=36, color=RED).next_to(dot, UP)
        
        def update_dot(d):
            d.move_to(axes.i2gp(tracker.get_value(), graph))
            
        def update_number(n):
            val = int(curve_func(tracker.get_value()))
            new_text = Text(str(val), font_size=36, color=RED)
            new_text.next_to(dot, UP)
            n.become(new_text)

        dot.add_updater(update_dot)
        number_display.add_updater(update_number)

        # 5. L'ANIMATION
        self.play(
            Write(axes), 
            Write(y_labels), 
            Write(date_start), 
            Write(date_mid), 
            Write(date_end), 
            Write(y_title)
        )
        
        self.add(dot, number_display)
        self.play(
            Create(graph),
            tracker.animate.set_value(total_days),
            run_time=5,
            rate_func=linear
        )
        
        # on force l'affichage du chiffre exact à la toute fin
        final_text = Text(str(final_views), font_size=36, color=RED).next_to(dot, UP)
        self.remove(number_display)
        self.add(final_text)
        
        final_box = SurroundingRectangle(final_text, color=YELLOW, buff=0.2)
        self.play(Create(final_box), FadeOut(final_box, run_time=0.5))
        self.wait(1)