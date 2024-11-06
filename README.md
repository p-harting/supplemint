# Supplemint
## Introduction
Welcome to **Supplemint**, the premier online destination for high-quality nutritional supplements! Our e-commerce platform, built with the robust capabilities of Django, is designed to provide health enthusiasts and wellness seekers with a seamless shopping experience. From vitamins to protein powders, we offer a curated range of products to support your journey toward optimal health and well-being.

This project was developed as part of a full-stack web development course, showcasing a comprehensive application of Django, Python, the Stripe API for secure and efficient payment processing, and advanced web development best practices.

![mockup](documentation/screenshots/mockup.png)

### View the live website [here](https://supplemint-91663a1226fd.herokuapp.com/)

## User Benefits

At **Supplemint**, we’re dedicated to enhancing your health journey with a diverse selection of high-quality supplements and a smooth, enjoyable shopping experience. Our platform caters to health and wellness enthusiasts, offering everything you need in one place. Here’s what makes Supplemint the ideal choice for your supplement needs:

### Superior Product Selection

-   **Extensive Categories**: Discover a wide variety of supplements organized for easy browsing:
    -   **Vitamins**: Essential nutrients to support your immune system and overall health.
    -   **Proteins**: High-quality protein powders and bars to aid in muscle recovery and boost performance.
    -   **Superfoods**: Nutrient-rich options like spirulina, acai, and chia seeds for overall wellness.
    -   **Herbs & Extracts**: A selection of botanical extracts to promote energy and vitality.
    -   **Vitalstoffe**: A comprehensive collection of essential micronutrients to enhance bodily functions.
-   **Subcategories for Easy Navigation**: Further refine your search within each category to quickly locate specific supplements.

### Detailed Product Information

-   **Comprehensive Product Details**: Each product page includes essential information, such as a descriptive title, thorough overview, price, available sizes, current stock levels, and user ratings. This way, you can make well-informed decisions.
-   **Customer Ratings and Reviews**: Read real reviews and ratings from other customers to better understand each product's benefits and effectiveness.

### Effortless Search and Sorting

-   **Smart Search Bar**: Quickly find what you’re looking for with our efficient search functionality.
-   **Flexible Sorting Options**: Organize products by name, price, or rating to streamline your shopping experience and discover what suits your needs.

### Personalized User Experience

-   **User Accounts**: Create a personalized account to unlock a range of features, including:
    -   Viewing and editing your profile.
    -   Checking your order history and tracking past purchases.
    -   Saving products to your wishlist for future consideration.

### Convenient Cart and Checkout

-   **Efficient Cart Management**: Add items to your cart, adjust quantities, or remove products with ease. Our intuitive checkout process ensures a smooth and secure transaction.
-   **Secure Payment Processing**: We use Stripe API to provide a fast and secure payment experience, safeguarding your personal and financial information.

### Engaging Community Features

-   **Custom Reviews and Ratings**: Share your experience and rate products to guide fellow shoppers. Your feedback helps create a trusted community of health-conscious individuals.
-   **Newsletter Subscription**: Stay informed and inspired by signing up for our newsletter. Receive health tips, product reviews, and exclusive deals directly to your inbox. Be the first to know about new arrivals and special promotions.

### Comprehensive Customer Support

-   **FAQ Section**: Access quick answers to common questions about our products, shipping, returns, and more through our extensive FAQ page.
-   **Contact Us**: If you need further assistance, our responsive support team is ready to help. Reach out via our Contact Us page to get personalized support.

### Transparent and Secure Policies

-   **Terms and Conditions & Privacy Policy**: We prioritize your privacy and security. Our terms, conditions, and privacy policy are clearly outlined to ensure a transparent and trustworthy shopping environment.
-   **Legal Standards**: Our policies are crafted to protect your rights and provide you with a safe, reliable experience on our platform.

## Persona: Alex Martinez - The Wellness-Oriented Fitness Enthusiast

**Basic Information:**

-   **Name:** Alex Martinez
-   **Age:** 29
-   **Occupation:** Software Engineer
-   **Location:** Denver, Colorado
-   **Family Status:** Single, lives with a Labrador named Luna

**Background:**  
Alex is a software engineer at a growing tech startup, working a hybrid schedule that allows him to balance his passion for health and fitness with his demanding job. He has been a fitness enthusiast for years, with a particular interest in weightlifting, outdoor sports, and nutrition. Alex dedicates time every day to working out, meal prepping, and researching the best ways to enhance his well-being through diet and lifestyle. He often shares fitness and supplement advice on social media and stays active in online wellness forums to keep up with new trends and products.

**Demographics:**

-   **Income:** $90,000 annually
-   **Education:** Bachelor’s degree in Computer Science
-   **Lifestyle:** Health-focused, environmentally conscious, tech-savvy, and socially active
-   **Shopping Preferences:** Prefers online shopping for convenience and wide selection; values high-quality, trustworthy brands that align with his healthy lifestyle

**Goals and Needs:**

-   **Goals:**
    -   To discover effective, science-backed supplements that boost his athletic performance and overall health.
    -   To integrate sustainable products into his lifestyle, from supplements to environmentally-friendly packaging.
    -   To simplify his shopping experience with a well-designed website that provides detailed information, making it easy to choose the right products.
-   **Needs:**
    -   Access to a comprehensive range of supplements, including proteins, vitamins, superfoods, and herbal extracts, all in one place.
    -   Clear, science-based product descriptions and trustworthy customer reviews to guide his purchase decisions.
    -   User-friendly filtering options that help him sort supplements based on specific goals like muscle gain, energy, or immune support.

**Pain Points:**

-   Frustration with websites that offer poor navigation, making it hard to compare products or find what he needs.
-   Concern about the environmental impact of supplement packaging and ingredients sourced unsustainably.
-   Difficulty finding reliable information about the ingredients and benefits of supplements, leading to hesitation in trying new products.

**Interests and Hobbies:**

-   Enjoys outdoor activities like hiking, rock climbing, and mountain biking, especially in the beautiful Colorado landscapes.
-   Avid weightlifter who follows a strict workout and dietary plan.
-   Interested in biohacking and regularly reads up on the latest research in health, fitness, and nutrition.
-   Volunteers occasionally at local community events focused on promoting health and wellness.

**Technology and Online Behavior:**

-   Regularly uses platforms like Instagram, Reddit, and YouTube to stay updated on health trends, new supplement launches, and workout tips.
-   Relies heavily on smartphone and tablet for browsing, making purchases, and tracking fitness progress through health apps.
-   Values in-depth product reviews and user testimonials to make informed decisions about what to buy.

**Reasons for Visiting the Website:**

-   **Comprehensive Product Range:** Alex is drawn to the diverse selection of high-quality supplements, from protein powders and vitamins to niche superfoods and herbal extracts, all in one convenient online store.
-   **Efficient and Smooth Experience:** He appreciates the intuitive search and sorting features, making it simple to filter products by goals, ratings, or ingredients.
-   **Detailed Insights and Transparency:** The site’s clear and comprehensive product descriptions, along with reviews from fellow health enthusiasts, give him confidence in his choices.

**Marketing Messages:**

-   "Fuel your fitness journey with our premium selection of supplements, crafted for maximum performance and well-being."
-   "Stay ahead of the health curve with our sustainable, science-backed products designed for the wellness-focused lifestyle."
-   "Shop smarter and healthier with a seamless online experience that delivers in-depth product insights and trustworthy reviews from fellow enthusiasts."
- 
This persona captures a typical Supplemint customer, focusing on their health-oriented mindset, online behaviors, and the seamless, transparent experience they seek from a supplement e-commerce platform.

## Technologies Used

### Backend

-   **Django (v5.1.1)**: The core framework for building our robust and scalable e-commerce platform, powering the entire backend infrastructure.
-   **ASGIref (v3.8.1)**: Ensures efficient asynchronous server and gateway interface functionality, enhancing real-time features and performance.
-   **Django Allauth (v64.2.1)**: A powerful authentication package that handles user sign-ups, logins, and account management with ease and security.
-   **Stripe**: Integrated for seamless and secure payment processing, enabling efficient handling of customer transactions.
-   **Standard Django Database**: Utilizing Django’s built-in database system for managing models, queries, and data efficiently.

### Image Generation

-   **SD-XL (Stability AI Model)**: Leveraged for AI-driven image generation, enhancing our product imagery and visual content. SD-XL is a state-of-the-art image synthesis model, bringing dynamic and high-quality visuals to our site.

### Database

-   **Django Internal Database**: A default and reliable database setup provided by Django, suitable for development and lightweight operations. It efficiently manages all backend data, from user information to product catalogs.
-   **SQLparse (v0.5.1)**: A non-GUI SQL parser used to format and analyze SQL queries within the project, aiding in cleaner database operations.

### Frontend

-   **Custom CSS and JavaScript**: Tailored styles and interactive features have been developed to provide a unique, engaging, and user-friendly interface.
-   **HTML and Responsive Design**: Focused on crafting a visually appealing and adaptive layout that looks great on any device without relying on frameworks like Bootstrap.

### Other Libraries & Tools

-   **pytz (v2024.2)**: Provides accurate and up-to-date time zone calculations, essential for managing time-based data across different regions.
-   **Stripe**: Secure and efficient API integration for processing payments, managing subscriptions, and ensuring financial data security.
-   **Pillow**: Used for image processing, handling tasks such as resizing and optimizing images uploaded to the platform.
-   **python-decouple**: Simplifies environment variable management, making configuration more secure and maintainable.
-   **Cryptography**: Implements secure data encryption and decryption, critical for protecting sensitive information.

### Deployment & Static File Management

-   **Whitenoise**: Enhances static file serving in production environments, ensuring fast and efficient delivery of CSS, JavaScript, and image assets.

## Features

### Product Categories

Explore our extensive selection of supplements, organized into intuitive categories and subcategories to help you quickly find what you’re looking for:

-   **Vitamins**: Essential nutrients like Vitamin D, Multivitamins, and specialty blends for immune support.
-   **Proteins**: High-quality whey, plant-based, and casein proteins in multiple flavors and formulations.
-   **Superfoods**: Nutrient-dense options including spirulina, matcha, acai, and chia seeds to boost your daily nutrition.
-   **Herbs & Extracts**: Natural botanicals such as Ashwagandha, Ginseng, and Turmeric for overall wellness.
-   **Vitalstoffe**: Comprehensive micronutrient solutions, like Magnesium, Zinc, and Omega-3 supplements.

Each category includes subcategories to refine your search, making it easy to locate specific types of supplements tailored to your health and fitness goals.

### Shopping Experience

Enjoy a seamless and efficient shopping journey with features designed to simplify your online experience:

-   **Product Sorting**: Easily sort products by name, price, and user rating in both ascending and descending order, ensuring you can view options that suit your preferences.
-   **Search Functionality**: Use our intuitive search bar to quickly find products by keyword, ensuring a smooth and efficient search experience.

### User Accounts

Manage your profile and keep track of your orders effortlessly:

-   **Profile Management**: Users can register, log in, and manage their personal details. Update or delete profile information as needed, and easily view a complete history of your orders.
-   **Order Details**: Get a detailed overview of each order, including product information, status, and payment confirmation.

### Cart and Checkout

A streamlined and user-friendly checkout process ensures a stress-free purchasing experience:

-   **Cart Details**: View all items in your cart at a glance, adjust quantities, remove products, or save items for later.
-   **Checkout**: A simple and secure checkout process that lets you enter shipping and payment information to complete your purchase efficiently.
-   **Order Confirmation**: Receive a comprehensive summary of your order, complete with an order number and the total amount paid, along with confirmation emails to keep you informed.

### Content Pages

Gain valuable insights and understand our policies to make informed shopping decisions:

-   **About Us**: Discover the mission behind Supplemint, our commitment to quality, and our passion for supporting a healthy lifestyle.
-   **Contact Us**: A simple contact form to reach out to our support team for any inquiries, concerns, or feedback.
-   **FAQ**: A comprehensive list of frequently asked questions to address common concerns about products, shipping, returns, and more.
-   **Terms and Conditions**: Review the terms governing the use of our website, from purchases to user conduct.
-   **Privacy Policies**: Learn how we handle and protect your personal data, emphasizing transparency and security.

### Loyalty Points System

Enjoy rewards for your loyalty with our exclusive points program:

-   **Earn Points**: Accumulate points for every purchase you make, rewarding you for investing in your health and wellness.
-   **Redeem Points**: Use your points for discounts on future orders, making it even more rewarding to shop with us.
-   **Track Points**: View your points balance and redemption history directly from your user profile.