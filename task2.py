import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF

# Load data with forward slashes
orders_df = pd.read_csv("C:/Users/ADMIN/OneDrive - Amity University/Documents/Yoshop.com/YoshopsAutomation_Task2/orders_2016-2020_Dataset.csv")
reviews_df = pd.read_csv("C:/Users/ADMIN/OneDrive - Amity University/Documents/Yoshop.com/YoshopsAutomation_Task2/review_dataset.csv")

# Clean numeric columns
orders_df['Subtotal'] = orders_df['Subtotal'].replace({'₹': '', ',': ''}, regex=True).astype(float)
orders_df['Shipping Cost'] = orders_df['Shipping Cost'].replace({'₹': '', ',': ''}, regex=True).astype(float)
orders_df['Discount'] = orders_df['Discount'].replace({'₹': '', ',': ''}, regex=True).astype(float)
orders_df['Total'] = orders_df['Total'].replace({'₹': '', ',': ''}, regex=True).astype(float)

# Convert date columns to datetime
orders_df['Order Date and Time Stamp'] = pd.to_datetime(orders_df['Order Date and Time Stamp'], format='%d-%m-%Y %H:%M:%S %z', errors='coerce', dayfirst=True)

# Helper function to save plots to PDF
def save_to_pdf(plots, filename):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for plot in plots:
        plt.savefig(f"{plot}.png")
        pdf.image(f"{plot}.png", x=10, w=190)
    pdf.output(f"{filename}.pdf")

# Analysis functions
def analysis_reviews_given_by_customers():
    review_counts = reviews_df['stars'].value_counts()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=review_counts.index, y=review_counts.values, palette='viridis')
    plt.title('Customer Reviews Distribution')
    plt.xlabel('Star Rating')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def analysis_payment_methods():
    payment_method_counts = orders_df['Payment Status'].value_counts()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=payment_method_counts.index, y=payment_method_counts.values, palette='Blues_d')
    plt.title('Distribution of Payment Methods')
    plt.xlabel('Payment Method')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.show()

def analysis_top_consumer_states():
    top_states = orders_df['Shipping State'].value_counts().nlargest(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_states.values, y=top_states.index, palette='Set2')
    plt.title('Top Consumer States in India')
    plt.xlabel('Number of Orders')
    plt.ylabel('States')
    plt.tight_layout()
    plt.show()

def analysis_top_consumer_cities():
    top_cities = orders_df['Shipping City'].value_counts().nlargest(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_cities.values, y=top_cities.index, palette='coolwarm')
    plt.title('Top Consumer Cities in India')
    plt.xlabel('Number of Orders')
    plt.ylabel('Cities')
    plt.tight_layout()
    plt.show()

def analysis_top_selling_categories():
    top_categories = orders_df['LineItem Name'].value_counts().nlargest(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_categories.values, y=top_categories.index, palette='magma')
    plt.title('Top Selling Product Categories')
    plt.xlabel('Number of Orders')
    plt.ylabel('Product Category')
    plt.tight_layout()
    plt.show()

def analysis_reviews_for_categories():
    category_reviews = reviews_df.groupby('category')['stars'].mean().nlargest(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=category_reviews.values, y=category_reviews.index, palette='chameleon')
    plt.title('Top Rated Product Categories')
    plt.xlabel('Average Star Rating')
    plt.ylabel('Product Category')
    plt.tight_layout()
    plt.show()

def analysis_orders_per_month_year():
    orders_df['Month_Year'] = orders_df['Order Date and Time Stamp'].dt.to_period('M')
    monthly_orders = orders_df.groupby('Month_Year')['Order #'].count()
    plt.figure(figsize=(12, 6))
    monthly_orders.plot(kind='line', marker='o', color='green')
    plt.title('Number of Orders Per Month Per Year')
    plt.xlabel('Month-Year')
    plt.ylabel('Number of Orders')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def analysis_reviews_orders_per_month_year():
    reviews_df['Month_Year'] = pd.to_datetime(reviews_df['stars']).dt.to_period('M')
    monthly_reviews = reviews_df.groupby('Month_Year')['stars'].count()
    plt.figure(figsize=(12, 6))
    monthly_reviews.plot(kind='line', marker='x', color='blue')
    plt.title('Reviews Per Month Per Year')
    plt.xlabel('Month-Year')
    plt.ylabel('Number of Reviews')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def analysis_orders_parts_of_day():
    orders_df['Hour'] = orders_df['Order Date and Time Stamp'].dt.hour
    parts_of_day = pd.cut(orders_df['Hour'], bins=[0, 6, 12, 18, 24], labels=['Night', 'Morning', 'Afternoon', 'Evening'])
    parts_of_day_counts = parts_of_day.value_counts()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=parts_of_day_counts.index, y=parts_of_day_counts.values, palette='inferno')
    plt.title('Orders Across Parts of the Day')
    plt.xlabel('Time of Day')
    plt.ylabel('Number of Orders')
    plt.tight_layout()
    plt.show()

# Main function to prompt user for analysis choice
def main():
    choice = int(input("Enter the number to see the analysis of your choice: "))
    
    if choice == 1:
        analysis_reviews_given_by_customers()
    elif choice == 2:
        analysis_payment_methods()
    elif choice == 3:
        analysis_top_consumer_states()
    elif choice == 4:
        analysis_top_consumer_cities()
    elif choice == 5:
        analysis_top_selling_categories()
    elif choice == 6:
        analysis_reviews_for_categories()
    elif choice == 7:
        analysis_orders_per_month_year()
    elif choice == 8:
        analysis_reviews_orders_per_month_year()
    elif choice == 9:
        analysis_orders_parts_of_day()
    elif choice == 10:
        plots = ['Reviews Given by Customers', 'Payment Methods', 'Top Consumer States', 'Top Consumer Cities', 
                 'Top Selling Categories', 'Reviews for Categories', 'Orders Per Month Year', 'Reviews Orders Per Month Year', 
                 'Orders Parts of Day']
        save_to_pdf(plots, 'Full_Report')

if __name__ == "__main__":
    main()