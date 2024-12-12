# WPI Course Recommender System

## CS547 Group Project

**Team Members**:  
Dante Amicarella, Adina Palayoor, Alisha Peeriz, Emre Sabaz, Arturo Lemos

---

## Introduction

Our team set out to build a course planning tool for WPI students that aids in their selection of classes to fulfill degree requirements. Unlike the available WPI planner tool, this system integrates course ratings and student rankings. 

### Key Objectives:
- Help students create a schedule that fulfills their major requirements.
- Provide insights into the difficulty and time commitment of available courses.
- Consolidate all relevant course information, including ratings, into a single platform.  

By simplifying the course planning process, we aim to alleviate student stress and improve decision-making.

---

## Data Sources

### 1. **OSCAR (Online Students Course Reports)**  
An interactive Tableau dashboard aggregating student feedback on courses and professors.  
**Metrics Include**:
- Average time spent on courses.
- Predicted grades.
- Professor evaluations.

### 2. **Workday WPI**  
A cloud-based platform that integrates administrative and academic processes.  
**Usage**: Extracted course information for the 2023-2024 academic year.

### 3. **RateMyProfessor (RMP)**  
An online platform for student reviews of professors.  
**Metrics Include**:
- Clarity and engagement.
- Workload and grading fairness.
- Overall helpfulness.

**[Link to Data Repository](https://github.com/amicarellade/WPI-Student-Course-Optimization-23-24)**  

---

## Data Retrieval

### OSCAR  
Due to its Tableau interface, standard web scraping techniques were insufficient. We used a combination of:  
- **Computer Vision**: To analyze and interpret ordered pixels from screenshots.  
- **Automation Tools**: For clicking, scrolling, and capturing screenshots.

### Workday  
Utilized a Python script with Selenium for web scraping:  
- Automated login and navigation.
- Extracted course and professor data using specific XPATHs.
- Continuous scrolling to load and retrieve all data.
- Saved extracted information into CSV files.

### RateMyProfessor  
Similar techniques to OSCAR were employed:  
- Computer vision and automated scrolling.  
- Analysis of screenshots for extracting professor ratings and comments.

---

## Running the Code

1. Clone the repository from [GitHub](https://github.com/amicarellade/WPI-Student-Course-Optimization-23-24).
2. Refer to the `README.md` in the repository for detailed setup and execution instructions.

---

## Conclusions

- Able to build upon a previous MQP that creates student schedules based on degree requirements
- Learned how to Webscrape workday, WPI Oscar and RateMyProfessor
- Reconfigured the HTML file to be able to improve the functionality of the output
- Was successful in outputting the course sections and professor ratings

## Future Work
- Add recommendation system to determine which specific sections students should take based off of the classes they need to take and the reviews
- Improving the design of the course recommendation tool
- Add more courses and professors past the CS, DS and MA courses at WPI

---

## References

- WPI Academic Resources  
- Online Students Course Reports (OSCAR)  
- Workday WPI  
- RateMyProfessor  
