from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox
import joblib

# -----------------------------
# App Settings
# -----------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# -----------------------------
# Load Model
# -----------------------------
try:
    model = joblib.load("model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
except Exception as e:
    messagebox.showerror("Error", f"Could not load model files.\n\n{e}")
    exit()

# -----------------------------
# Main Window
# -----------------------------
app = ctk.CTk()
app.title("Review Sentiment Analyzer")
app.geometry("1100x700")
app.minsize(1000, 650)

# -----------------------------
# Colors
# -----------------------------
BG = "#E5E7EB"
CARD = "#F1F5F9"
BLUE = "#2563EB"
GREEN = "#22C55E"
RED = "#EF4444"
ORANGE = "#F59E0B"
TEXT = "#F8FAFC"
LIGHT = "#CBD5E1"

app.configure(fg_color=BG)




# -----------------------------
# Global Variables
# -----------------------------
total_count = 0
positive_count = 0
negative_count = 0

last_prediction = ""
last_confidence = 0
history = []

current_mode="dark"
current_prediction=""
current_confidence=0
# -----------------------------
# Functions
# -----------------------------


def clear_all():

    review_box.delete("1.0", "end")

    prediction_label.configure(
        text="Waiting...",
        text_color=LIGHT
    )

    confidence_label.configure(text="0.00%")

    confidence_status.configure(
        text="No confidence available",
        text_color="gray70"
    )

    

    progress.set(0)

    status_label.configure(text="🟢 Ready")
def reset_statistics():

    global total_count, positive_count, negative_count

    total_count = 0
    positive_count = 0
    negative_count = 0

    total_reviews.configure(
        text="📝 Reviews Analyzed\n0"
    )

    positive_reviews.configure(
        text="😊 Positive\n0"
    )

    negative_reviews.configure(
        text="😞 Negative\n0"
    )

    status_label.configure(
        text="📊 Statistics Reset"
    )
    history.clear()

    history_box.configure(state="normal")
    history_box.delete("1.0", "end")
    history_box.insert("1.0", "No history available...")
    history_box.configure(state="disabled")

def save_result():

    if prediction_label.cget("text") == "Waiting...":
        messagebox.showwarning(
            "Warning",
            "No result available to save."
        )
        return

    filename = "Sentiment_Result.txt"

    with open(filename, "a", encoding="utf-8") as file:

        file.write("="*50 + "\n")
        file.write(f"Review:\n{review_box.get('1.0','end').strip()}\n\n")
        file.write(f"Prediction : {prediction_label.cget('text')}\n")
        file.write(f"Confidence : {confidence_label.cget('text')}\n")
        file.write(f"Time : {datetime.now().strftime('%d-%m-%Y %I:%M %p')}\n")
        file.write("="*50 + "\n\n")

    messagebox.showinfo(
        "Saved",
        "Result saved successfully."
    )

def exit_app():
    app.destroy()

    
def toggle_theme():
    global current_mode

    if current_mode == "dark":

        ctk.set_appearance_mode("light")
        current_mode = "light"

        theme_btn.configure(
            text="🌙 Dark Mode",
            fg_color="#D67AF7",
            hover_color="#6D28D9"
        )

        # Review box light mode
        review_box.configure(
            fg_color="#EAE7E7",
            text_color="#111827"
        )


    else:

        ctk.set_appearance_mode("dark")
        current_mode = "dark"

        theme_btn.configure(
            text="☀️Light Mode",
            fg_color="#673B43",
            hover_color="#672130"
        )

        # Review box dark mode
        review_box.configure(
            fg_color="#111827",
            text_color="white"
        )


# ===============================
# ANALYSIS REPORT
# ===============================
def show_report():

    if prediction_label.cget("text") == "Waiting...":
        messagebox.showwarning(
            "Warning",
            "Please analyze a review first."
        )
        return

    popup = ctk.CTkToplevel(app)
    popup.title("Analysis Report")
    popup.geometry("520x650")
    popup.update_idletasks()

    x = app.winfo_x() + (app.winfo_width() // 2) - (520 // 2)
    y = app.winfo_y() + (app.winfo_height() // 2) - (650 // 2)

    popup.geometry(f"520x650+{x}+{y}")
    popup.resizable(False, False)
    popup.configure(fg_color="#F8FAFC")

    # ==========================
    # Title
    # ==========================
    title = ctk.CTkLabel(
        popup,
        text="📄 Analysis Report",
        font=("Arial",24,"bold"),
        text_color="#1E3A8A"
    )
    title.pack(pady=(20,15))

    review = review_box.get("1.0","end").strip()

    words = len(review.split())
    characters = len(review)
    sentences = review.count(".") + review.count("?") + review.count("!")

    prediction = prediction_label.cget("text")
    confidence = confidence_label.cget("text")

    if "POSITIVE" in prediction:
        pred_color = "#16A34A"
        recommendation = "Customer feedback is positive.\nMaintain the current quality.\n"
    else:
        pred_color = "#DC2626"
        recommendation = "Customer feedback is negative.\nReview customer concerns."

    report = ctk.CTkTextbox(
        popup,
        width=470,
        height=490,
        font=("Arial",14),
        corner_radius=12
    )
    report.pack(padx=20)

    report.insert("end","📝 REVIEW INFORMATION\n")
    report.insert("end","━━━━━━━━━━━━━━━━━━━━━━\n")
    report.insert("end",f"Words        : {words}\n")
    report.insert("end",f"Characters   : {characters}\n")
    report.insert("end",f"Sentences    : {sentences}\n\n\n")

    report.insert("end","🤖 SENTIMENT RESULT\n")
    report.insert("end","━━━━━━━━━━━━━━━━━━━━━━\n")
    report.insert("end",f"Prediction   : {prediction}\n")
    report.insert("end",f"Confidence   : {confidence}\n\n\n")

    report.insert("end","⚙ MODEL INFORMATION\n")
    report.insert("end","━━━━━━━━━━━━━━━━━━━━━━\n")
    report.insert("end","Algorithm    : Naive Bayes\n")
    report.insert("end","Status       : Completed Successfully\n\n\n")

    report.insert("end","📊 ANALYSIS STATISTICS\n")
    report.insert("end","━━━━━━━━━━━━━━━━━━━━━━\n")
    report.insert("end",f"Reviews      : {total_count}\n")
    report.insert("end",f"Positive     : {positive_count}\n")
    report.insert("end",f"Negative     : {negative_count}\n\n\n")

    report.insert("end","🕒 ANALYSIS TIME\n")
    report.insert("end","━━━━━━━━━━━━━━━━━━━━━━\n")
    report.insert("end",datetime.now().strftime("%d %b %Y | %I:%M %p"))
    report.insert("end","\n\n\n")

    report.insert("end","💡 RECOMMENDATION\n")
    report.insert("end","━━━━━━━━━━━━━━━━━━━━━━\n")
    report.insert("end",recommendation)

    report.configure(state="disabled")

    close_btn = ctk.CTkButton(
        popup,
        text="Close",
        width=120,
        fg_color="#2563EB",
        hover_color="#1D4ED8",
        command=popup.destroy
    )

    close_btn.pack(pady=20)

    
def show_about():

    popup = ctk.CTkToplevel(app)
    popup.title("About")
    popup.geometry("420x320")
    popup.resizable(False, False)

    popup.transient(app)
    popup.grab_set()
    popup.focus_force()

    title = ctk.CTkLabel(
        popup,
        text="ℹ About",
        font=("Arial",22,"bold")
    )
    title.pack(pady=(20,10))

    info = ctk.CTkLabel(
        popup,
        text=(
            "Review Sentiment Analyzer\n\n"
            "Version : 1.0\n"
            "Algorithm : Multinomial Naive Bayes\n"
            "GUI : CustomTkinter\n\n"
            "Developed by:\n"
            "Sidra Khan\n\n"
            "AI/ML Internship Project\n"
            "M Tech Production"
        ),
        font=("Arial",14),
        justify="center"
    )
    info.pack(pady=10)

    close_btn = ctk.CTkButton(
        popup,
        text="Close",
        width=100,
        command=popup.destroy
    )
    close_btn.pack(pady=15)

    # ===================================================
# LEFT PANEL
# ===================================================

left_frame = ctk.CTkFrame(
    app,
    width=300,
    corner_radius=0,
    fg_color="#0C5879"
)
left_frame.pack(side="left", fill="y")
left_frame.pack_propagate(False)


logo = ctk.CTkLabel(
    left_frame,
    text="🧠",
    font=("Segoe UI Emoji", 70)
)
logo.pack(pady=(25,10))

title = ctk.CTkLabel(
    left_frame,
    text="Review Sentiment\nAnalyzer",
    font=("Arial",30,"bold"),
    justify="center"
)
title.pack()



# ==========================
# Analysis Statistics
# ==========================

stats_title = ctk.CTkLabel(
    left_frame,
    text="📊 Analysis Statistics",
    font=("Arial",17,"bold"),
    text_color="#FACC15"
)
stats_title.pack(pady=(20,10))

total_reviews = ctk.CTkLabel(
    left_frame,
    text="📝 Reviews Analyzed\n0",
    font=("Arial",14, "bold")
)
total_reviews.pack(pady=5)

positive_reviews = ctk.CTkLabel(
    left_frame,
    text="😊 Positive\n0",
    font=("Arial",14, "bold"),
    text_color="#22C55E"
)
positive_reviews.pack(pady=5)

negative_reviews = ctk.CTkLabel(
    left_frame,
    text="😞 Negative\n0",
    font=("Arial",14, "bold"),
    text_color="#EF4444"
)
negative_reviews.pack(pady=5)
reset_stats_btn = ctk.CTkButton(
    left_frame,
    text="🔄 Reset Statistics",
    width=180,
    height=40,
    fg_color="#2563EB",
    hover_color="#1D4ED8",
    command=reset_statistics
)

reset_stats_btn.pack(

    pady=(10,20)
)
history_title = ctk.CTkLabel(
    left_frame,
    text="📝 Recent History",
    font=("Arial",16,"bold"),
    text_color="#FACC15"
)

history_title.pack(pady=(25,5))


history_box = ctk.CTkTextbox(
    left_frame,
    width=220,
    height=130,
    corner_radius=10,
    font=("Arial",12)
)

history_box.pack(
    padx=20
)

history_box.insert(
    "1.0",
    "No history available..."
)

history_box.configure(
    state="disabled"
)



# ===================================================
# RIGHT PANEL
# ===================================================


right_frame = ctk.CTkFrame(
    app,
    fg_color=BG,
    corner_radius=0
)

right_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(40,0)
)

heading = ctk.CTkLabel(
    right_frame,
    text="Customer Review Analysis",
    font=("Arial",30,"bold"),
    text_color="#1F2937"
)
heading.pack(pady=(30,10))




# ===================================================
# INPUT BOX
# ===================================================

input_frame = ctk.CTkFrame(
    right_frame,
    fg_color="#969698",
    corner_radius=15
)
input_frame.pack(
    padx=50,
    pady=15,
    fill="x"
)

input_title = ctk.CTkLabel(
    input_frame,
    text="Customer Review",
    font=("Arial",17,"bold"),
    text_color="#1F2937",
)
input_title.pack(anchor="w", padx=20, pady=(10,4))

review_box = ctk.CTkTextbox(
    input_frame,
    width=700,
    height=100,
    font=("Arial",16),
    corner_radius=12,
    fg_color="#EAE7E7",
    text_color="#111827",
)
review_box.pack(
    padx=20,
    pady=(0,20),
    fill="x"
)



# ===================================================
# BUTTONS
# ===================================================

button_frame = ctk.CTkFrame(
    right_frame,
    fg_color="transparent"
)
button_frame.pack(pady=10)
theme_btn = ctk.CTkButton(
    button_frame,
    text="🌙 Theme",
    width=120,
    height=40,
    fg_color="#DA3B9A",
    hover_color="#C416A1",
    font=("Arial",14,"bold"),
    command=toggle_theme
)
theme_btn.grid(row=0, column=0, padx=6)

analyze_btn = ctk.CTkButton(
    button_frame,
    text="🔍 Analyze",
    width=120,
    height=40,
    fg_color=BLUE,
    hover_color="#1D4ED8",
    font=("Arial",16,"bold"),
    command= lambda: analyze_review()
)
analyze_btn.grid(row=0,column=1,padx=6)

clear_btn = ctk.CTkButton(
    button_frame,
    text="🧹 Clear",
    width=120,
    height=40,
    fg_color=ORANGE,
    hover_color="#F5BA77",
    font=("Arial",16,"bold"),
    command=clear_all
)
clear_btn.grid(row=0,column=2,padx=6)

save_btn = ctk.CTkButton(
    button_frame,
    text="💾 Save",
    width=120,
    height=40,
    fg_color="#10B981",
    hover_color="#059669",
    font=("Arial",16,"bold"),
    command=save_result
)

save_btn.grid(row=0,column=3,padx=6)

exit_btn = ctk.CTkButton(
    button_frame,
    text="❌ Exit",
    width=120,
    height=40,
    fg_color=RED,
    hover_color="#DC2626",
    font=("Arial",16,"bold"),
    command=exit_app
)
exit_btn.grid(row=0,column=4,padx=6)

report_btn = ctk.CTkButton(
    button_frame,
    text="📄 Report",
    width=120,
    height=40,
    fg_color="#7C3AED",
    hover_color="#6D28D9",
    font=("Arial",14,"bold"),
    command=show_report
)

report_btn.grid(row=0, column=6, padx=6)

# ===================================================
# RESULT SECTION
# ===================================================

result_frame = ctk.CTkFrame(
    right_frame,
    fg_color=CARD,
    corner_radius=20,
    border_width=2,
    border_color="#334155"
)
result_frame.pack(
    padx=25,
    pady=10,
    fill="x"
)


result_title = ctk.CTkLabel(
    result_frame,
    text="AI Sentiment Analysis Result",
    font=("Arial",18,"bold"),
    text_color="#1F2937"
)
result_title.pack(pady=(20,10))


prediction_label = ctk.CTkLabel(
    result_frame,
    text="Waiting...",
    font=("Arial",30,"bold"),
    text_color="#2E3E54"

)
prediction_label.pack(pady=8)


confidence_status = ctk.CTkLabel(
    result_frame,
    text="No confidence available",
    font=("Arial",17,"bold"),
    text_color="#1399A3"
)
confidence_status.pack()


confidence_heading = ctk.CTkLabel(
    result_frame,
    text="📊 Confidence",
    font=("Arial",17,"bold"),
    text_color="#1F2937"
)
confidence_heading.pack(pady=(15,5))


confidence_label = ctk.CTkLabel(
    result_frame,
    text="0.00%",
    font=("Arial",20,"bold"),
    text_color="#38BDF8"
)
confidence_label.pack()


progress = ctk.CTkProgressBar(
    result_frame,
    width=430,
    height=12,
    corner_radius=10
)
progress.pack(pady=(5,10))

progress.set(0)

about_btn = ctk.CTkButton(
    result_frame,
    text="ℹ About",
    width=120,
    height=35,
    fg_color="#475569",
    hover_color="#334155",
    font=("Arial",13,"bold"),
    command=show_about
)

about_btn.pack(pady=(10,15))

progress.configure(
    progress_color="#2563EB",
    fg_color="#CBD5E1"
)



# Divider
divider = ctk.CTkFrame(
    result_frame,
    height=1,
    fg_color="#475569"
)
divider.pack(
    fill="x",
    padx=25,
    pady=5
)


# ===================================================
# STATUS BAR
# ===================================================

status_frame = ctk.CTkFrame(
    app,
    height=45,
    corner_radius=0,
    fg_color="#111827"
)

status_frame.pack(
    side="bottom",
    fill="x"
)


status_label = ctk.CTkLabel(
    status_frame,
    text="🟢 Ready",
    font=("Arial",12)
)

status_label.pack(
    side="left",
    padx=18
)


version_label = ctk.CTkLabel(
    status_frame,
    text="AI Sentiment Analyzer v1.0",
    font=("Arial",12),
    text_color="gray70"
)

version_label.pack(
    side="right",
    padx=30
)



# ===================================================
# UPDATE PREDICTION FUNCTION
# ===================================================


def analyze_review():

    global total_count, positive_count, negative_count, history
    global current_prediction, current_confidence

    review = review_box.get("1.0", "end").strip()

    if review == "":
        messagebox.showwarning(
            "Warning",
            "Please enter a review."
        )
        return

    status_label.configure(
        text="🔄 Analyzing Review..."
    )

    review_vector = vectorizer.transform([review])

    prediction = model.predict(review_vector)[0]

    # -----------------------------
    # Update Statistics
    # -----------------------------
    total_count += 1

    if prediction.lower() == "positive":
        positive_count += 1
        emoji = "😊"
        color = "#22C55E"
        message = (
            "The review is classified as Positive.\n"
            "The model detected a positive customer opinion."
        )
    else:
        negative_count += 1
        emoji = "😞"
        color = "#EF4444"
        message = (
            "The review is classified as Negative.\n"
            "The model detected a negative customer opinion."
        )

    total_reviews.configure(
        text=f"📝 Reviews Analyzed\n{total_count}"
    )

    positive_reviews.configure(
        text=f"😊 Positive\n{positive_count}"
    )

    negative_reviews.configure(
        text=f"😞 Negative\n{negative_count}"
    )

    # -----------------------------
    # Confidence
    # -----------------------------
    confidence = model.predict_proba(review_vector).max() * 100
    current_prediction= prediction
    current_confidence= confidence

    progress.set(confidence / 100)

    prediction_label.configure(
        text=f"{emoji} {prediction.upper()}",
        text_color=color
    )

    confidence_label.configure(
        text=f"{confidence:.2f}%"
    )

    if confidence >= 85:
        confidence_status.configure(
            text="🟢 Very High Confidence",
            text_color="#22C55E"
        )

    elif confidence >= 70:
        confidence_status.configure(
            text="🟢 High Confidence",
            text_color="#22C55E"
        )

    elif confidence >= 55:
        confidence_status.configure(
            text="🟡 Moderate Confidence",
            text_color="#EAB308"
        )

    else:
        confidence_status.configure(
            text="🔴 Low Confidence",
            text_color="#EF4444"
        )


    history_box.configure(state="normal")

    if history_box.get("1.0", "end").strip() == "No history available...":
       history_box.delete("1.0", "end")

    history_box.insert(
    "1.0",
    f"{emoji} {prediction.upper()} - {review[:25]}...\n"
)

    history_box.configure(state="disabled")

    # -----------------------------
    # History
    # -----------------------------
    history.append(
        f"{prediction.upper()} ({confidence:.2f}%)\n{review[:25]}..."
    )

    history_box.configure(state="normal")
    history_box.delete("1.0", "end")

    for item in reversed(history[-5:]):
        history_box.insert("end", item + "\n\n")

    history_box.configure(state="disabled")




analyze_btn.configure(
    command=analyze_review
)

# ===================================================
# START APPLICATION
# ===================================================

app.mainloop()
