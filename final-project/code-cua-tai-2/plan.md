# PLAN.md — C++ Interactive Learning & Knowledge Platform

## 0. Tên và định vị sản phẩm

**Tên tạm:** C++ Interactive Learning & Knowledge Platform

**Mục tiêu:** Xây dựng nền tảng web học và tra cứu kiến thức môn **Nhập môn lập trình bằng C++**, dành cho **người mới học**, kết hợp:

1. Knowledge Base có cấu trúc.
2. Tra cứu theo bài học.
3. Tra cứu theo loại kiến thức.
4. Tra cứu theo dạng bài tập và phương pháp giải.
5. Gợi ý kiến thức liên quan bằng Knowledge Graph + Recommendation Engine.
6. Interactive visualization.
7. C++ code execution và execution trace.
8. Bài tập, hướng dẫn, quiz.
9. AI Tutor thông qua API LLM do người quản trị tự host.
10. AI Problem Recognition và AI Debug/Explain.
11. Learning Path và theo dõi tiến độ.

Tham khảo trải nghiệm tương tác từ VisuAlgo nhưng **không sao chép giao diện, mã nguồn hoặc nội dung**.

---

# 1. Nguyên tắc sản phẩm

## 1.1. Database-first

Knowledge Base là nguồn kiến thức chính.

Luồng tra cứu mặc định:

```text
User Query
    ↓
Query Processing
    ↓
Database Search
    ├── Full-text
    ├── Fuzzy
    ├── Tag
    ├── Exact concept
    ├── Relation
    └── Semantic/vector search
    ↓
Rank Results
    ↓
Return Knowledge
```

Không gửi mọi truy vấn cho LLM.

## 1.2. AI là lớp hỗ trợ

LLM được dùng cho:

- Giải thích kiến thức.
- Tóm tắt.
- Gợi ý.
- Phân tích đề bài.
- Nhận diện dạng bài.
- Hướng dẫn debug.
- Explain code.
- Sinh quiz khi cần.
- Search fallback khi Knowledge Base không đủ thông tin.

LLM **không được xem là nguồn sự thật duy nhất**.

## 1.3. AI fallback phải có chủ đích

Nếu database search có confidence thấp:

```text
Search
  ↓
Không đủ kết quả
  ↓
Hiển thị:
"Không tìm thấy đầy đủ trong kho kiến thức.
Bạn có muốn thử AI không?"
  ↓
User xác nhận
  ↓
LLM
```

AI-generated content không tự động trở thành Knowledge Base.

Có thể lưu thành:

```text
AI Draft
   ↓
Admin Review
   ↓
Published Knowledge
```

## 1.4. Người học phải được dẫn dắt

Khi làm bài, hệ thống ưu tiên:

```text
Nhận diện bài toán
→ Kiến thức cần thiết
→ Pattern
→ Phương pháp
→ Gợi ý
→ Tự viết code
→ Visualization
→ Lời giải
```

Không mặc định đưa đáp án ngay.

---

# 2. Đối tượng

Đối tượng chính:

- Người chưa biết lập trình.
- Sinh viên năm nhất.
- Người mới học C++.
- Người cần ôn tập Nhập môn lập trình.

Giải thích phải ưu tiên:

- Ngôn ngữ đơn giản.
- Ví dụ cụ thể.
- Visualization.
- Từng bước.
- Giải thích "tại sao", không chỉ "làm thế nào".

---

# 3. Phạm vi kiến thức

Ngôn ngữ chính:

**C++**

Giai đoạn đầu tập trung vào C++ cơ bản, không cố gắng bao phủ toàn bộ C++ hiện đại.

## 3.1. Syllabus đề xuất

```text
01. Làm quen với lập trình
    ├── Chương trình là gì
    ├── Thuật toán
    ├── Compiler
    ├── Source code
    ├── C++ program structure
    └── Compile / Run

02. Biến và kiểu dữ liệu
    ├── Variable
    ├── Constant
    ├── int
    ├── float
    ├── double
    ├── char
    ├── bool
    ├── string
    ├── Declaration
    ├── Initialization
    └── Type conversion

03. Input / Output
    ├── cout
    ├── cin
    ├── getline
    ├── Formatting
    └── Input validation cơ bản

04. Toán tử và biểu thức
    ├── Arithmetic
    ├── Assignment
    ├── Comparison
    ├── Logical
    ├── Increment / Decrement
    ├── Precedence
    └── Expression

05. Cấu trúc rẽ nhánh
    ├── if
    ├── if / else
    ├── else if
    ├── nested if
    ├── switch
    ├── Conditional operator
    └── Multiple conditions

06. Vòng lặp
    ├── for
    ├── while
    ├── do while
    ├── break
    ├── continue
    ├── Nested loops
    └── Loop invariant cơ bản

07. Hàm
    ├── Function
    ├── Parameter
    ├── Return value
    ├── void
    ├── Local / global variable
    ├── Scope
    ├── Pass by value
    └── Function decomposition

08. Mảng
    ├── One-dimensional array
    ├── Index
    ├── Traversal
    ├── Input / output array
    ├── Search
    ├── Max / Min
    ├── Sum / Average
    ├── Count
    ├── Insert
    ├── Delete
    └── Reverse

09. Chuỗi
    ├── char
    ├── C-string ở mức cơ bản
    ├── std::string
    ├── Traversal
    ├── Search character
    ├── Count
    ├── Compare
    ├── Normalize
    └── Palindrome

10. Số học cơ bản
    ├── Even / Odd
    ├── Divisor
    ├── Multiple
    ├── Prime
    ├── GCD
    ├── LCM
    ├── Digit extraction
    ├── Reverse number
    └── Special numbers

11. Thuật toán cơ bản
    ├── Linear Search
    ├── Binary Search
    ├── Bubble Sort
    ├── Selection Sort
    ├── Insertion Sort
    └── Basic complexity intuition

12. Đệ quy
    ├── Recursive function
    ├── Base case
    ├── Recursive case
    ├── Call stack
    ├── Factorial
    ├── Fibonacci
    └── Simple recursive problems

13. STL cơ bản
    ├── vector
    ├── pair
    ├── string
    ├── sort
    ├── find
    ├── reverse
    └── Basic iterator concept
```

Syllabus phải được lưu dưới dạng dữ liệu, không hard-code trong frontend.

---

# 4. Information Architecture

```text
Course
 └── Chapter
      └── Lesson
           └── Topic
                ├── Concept
                ├── Definition
                ├── Property
                ├── Rule
                ├── Syntax
                ├── Example
                ├── Pattern
                ├── Algorithm
                ├── Exercise
                ├── Common Mistake
                └── Related Knowledge
```

Một Topic có thể xuất hiện trong nhiều Lesson thông qua relation, không duplicate nội dung.

---

# 5. Knowledge Taxonomy

Mỗi knowledge item có `type`.

Các type tối thiểu:

```text
CONCEPT
DEFINITION
PROPERTY
RULE
SYNTAX
PATTERN
ALGORITHM
TECHNIQUE
EXAMPLE
COUNTER_EXAMPLE
COMMON_MISTAKE
EXERCISE
SOLUTION
QUIZ
```

## 5.1. Concept

Ví dụ:

```text
Variable
Array
Loop
Function
Recursion
```

## 5.2. Property

Ví dụ:

```text
Array:
- Các phần tử cùng kiểu.
- Có thể truy cập bằng index.
- Kích thước array tĩnh được xác định khi khai báo.
```

## 5.3. Pattern

Pattern là mẫu tư duy giải bài.

Ví dụ:

```text
Accumulator
Counter
Linear Scan
Maintain Best Candidate
Flag
Sentinel
Frequency Counting
Nested Iteration
Two Variables
Two Pointers
Brute Force
Recursion
```

Pattern phải có:

- Mục đích.
- Khi nào sử dụng.
- Dấu hiệu nhận biết.
- Pseudocode.
- Code mẫu.
- Bài tập áp dụng.
- Pattern liên quan.
- Lỗi thường gặp.

---

# 6. Taxonomy dạng bài tập

Exercise phải được phân loại nhiều chiều.

## 6.1. Arithmetic

```text
Tính tổng
Tính tích
Tính trung bình
Tính biểu thức
Tính theo công thức
```

## 6.2. Conditional

```text
Kiểm tra điều kiện
Phân loại
So sánh
Max / Min
Kiểm tra hợp lệ
Xét nhiều trường hợp
```

## 6.3. Counting

```text
Đếm phần tử
Đếm phần tử thỏa điều kiện
Đếm chẵn / lẻ
Đếm số nguyên tố
Đếm chữ số
Đếm tần suất
```

## 6.4. Aggregation

```text
Sum
Product
Average
Max
Min
Count
Frequency
```

## 6.5. Searching

```text
Linear Search
Binary Search
Find First
Find Last
Find Position
Search by Condition
```

## 6.6. Array

```text
Traversal
Input / Output
Max / Min
Sum
Count
Reverse
Insert
Delete
Search
Sort
```

## 6.7. String

```text
Traversal
Count Character
Search Character
Compare
Normalize
Palindrome
```

## 6.8. Number Theory

```text
Even / Odd
Prime
Divisor
Multiple
GCD
LCM
Digit Processing
Special Number
```

## 6.9. Recursion

```text
Factorial
Fibonacci
Recursive Sum
Recursive Search
Divide Problem
```

## 6.10. Algorithmic Patterns

```text
Accumulator
Counter
Linear Scan
Maintain Best
Flag / Sentinel
Frequency Counting
Nested Iteration
Brute Force
Recursion
```

Một Exercise có thể có nhiều classification.

---

# 7. Exercise Model

Mỗi bài tập phải chứa:

```text
id
title
statement
input
output
constraints
examples
difficulty
problem_types
patterns
required_knowledge
prerequisites
learning_objectives
hints
solution_strategy
pseudocode
reference_solution
common_mistakes
visualization
related_exercises
tags
```

Difficulty:

```text
BEGINNER
EASY
MEDIUM
HARD
```

Không chỉ dựa vào độ dài code; difficulty phải dựa trên kiến thức, số bước suy luận và mức độ kết hợp pattern.

---

# 8. Solution Strategy

Lời giải phải tách thành nhiều tầng.

```text
Problem
 ↓
Understand
 ↓
Identify Pattern
 ↓
Plan
 ↓
Pseudocode
 ↓
Code
 ↓
Test
```

Ví dụ:

```text
Bài: Tìm max trong mảng

Pattern:
Maintain Best Candidate

Strategy:
1. Chọn phần tử đầu tiên làm max.
2. Duyệt các phần tử còn lại.
3. Nếu phần tử hiện tại lớn hơn max thì cập nhật.
4. In max.
```

---

# 9. Knowledge Graph

Quan hệ phải là dữ liệu có hướng.

Các relation:

```text
PREREQUISITE
RELATED
NEXT
SIMILAR
PRACTICE
PATTERN
EXAMPLE
COMMON_MISTAKE
CONTRAST
PART_OF
USED_BY
LEADS_TO
REQUIRES
SOLVES
```

Ví dụ:

```text
Find Maximum
    ├── REQUIRES → Array
    ├── REQUIRES → Loop
    ├── REQUIRES → Comparison
    ├── PATTERN → Linear Scan
    ├── SIMILAR → Find Minimum
    ├── RELATED → Find Maximum Position
    └── PRACTICE → Find Max Exercise
```

---

# 10. Knowledge Recommendation Engine

Đây là module bắt buộc.

Không chỉ hiển thị danh sách `related`.

## 10.1. Recommendation categories

```text
Nên biết trước
Học tiếp
Kiến thức liên quan
Kiến thức tương tự
Dạng bài tương tự
Phương pháp liên quan
Ví dụ liên quan
Lỗi thường gặp
```

## 10.2. Context-aware recommendation

Recommendation thay đổi theo context:

```text
Topic page
Exercise page
Code editor
Quiz
AI Tutor
Search result
Learning path
```

Ví dụ khi xem "Tìm Max":

```text
Nên biết trước:
- Variable
- Array
- Loop
- Comparison

Học tiếp:
- Find Minimum
- Find Position of Maximum
- Conditional Maximum

Pattern:
- Linear Scan
- Maintain Best Candidate
```

## 10.3. Recommendation ranking

Ranking nội bộ dựa trên:

```text
relation type
graph distance
same lesson
same topic
same pattern
prerequisite relation
exercise context
user progress
```

Có thể dùng score:

```text
score =
    relation_score
  + graph_distance_score
  + context_score
  + topic_score
  + pattern_score
  + progress_score
```

Trọng số phải configurable.

Không hiển thị score nội bộ cho người dùng.

## 10.4. Why recommended

Mỗi recommendation phải có thể giải thích:

```text
Tại sao được gợi ý?

"Vòng lặp for" được gợi ý vì
bài toán Tìm Max cần duyệt qua
các phần tử trong mảng.
```

Nếu có thể, hiển thị đường đi trong graph:

```text
Find Max
  ↓ requires
Array Traversal
  ↓ requires
Loop
```

---

# 11. Interactive Knowledge Graph UI

Topic page có khu vực:

```text
Khám phá kiến thức liên quan
```

Cho phép:

- Zoom.
- Pan.
- Click node.
- Highlight current node.
- Highlight prerequisites.
- Highlight next knowledge.
- Navigate sang topic khác.

Không render toàn bộ graph mặc định.

Chỉ render neighborhood của node hiện tại.

---

# 12. Search System

Search là tính năng cốt lõi.

## 12.1. Search modes

```text
Exact
Keyword
Full-text
Fuzzy
Tag
Semantic
Relation-aware
```

## 12.2. Search result categories

```text
Tất cả
Bài học
Khái niệm
Tính chất
Pattern
Thuật toán
Bài tập
Phương pháp
Ví dụ
```

Ví dụ query:

```text
"cách tìm số lớn nhất trong mảng"
```

Kết quả:

```text
Concept:
- Array

Pattern:
- Linear Scan
- Maintain Best Candidate

Exercise:
- Tìm số lớn nhất

Method:
- MAX/MIN Scan
```

## 12.3. Ranking

Search ranking configurable:

```text
title match
keyword match
description match
tag match
exact match
semantic similarity
relation
lesson relevance
```

PostgreSQL được ưu tiên cho MVP:

```text
PostgreSQL FTS
pg_trgm
pgvector
```

Không bắt buộc Elasticsearch/OpenSearch ở MVP.

---

# 13. AI Search Fallback

Khi search không đạt threshold:

```text
Search Result
    ↓
Confidence < threshold
    ↓
UI:
"Không tìm thấy đủ thông tin.
Bạn có muốn hỏi AI không?"
```

User phải chủ động chọn AI.

AI response phải đánh dấu:

```text
AI-generated
```

Nếu AI sử dụng Knowledge Base:

```text
Sources
- Topic A
- Pattern B
- Exercise C
```

Nếu AI đưa kiến thức bên ngoài Knowledge Base, phải phân biệt rõ:

```text
From Knowledge Base
AI Generated / External
```

Không tự động publish.

---

# 14. AI Provider

LLM phải configurable qua Admin hoặc `.env`.

MVP sử dụng OpenAI-compatible API.

Configuration:

```text
LLM_BASE_URL
LLM_API_KEY
LLM_MODEL
LLM_TEMPERATURE
LLM_MAX_TOKENS
LLM_TIMEOUT
```

UI:

```text
AI Settings

Base URL
API Key
Model
Temperature
Max Tokens

[Test Connection]
```

Backend phải có abstraction:

```text
LLMProvider
    └── OpenAICompatibleProvider
```

Không hard-code nhà cung cấp cụ thể.

---

# 15. AI Tutor

Các mode:

```text
Explain
Hint
Analyze Problem
Explain Code
Debug
Generate Quiz
Ask About Topic
```

AI phải nhận context phù hợp:

```text
current topic
related knowledge
exercise
user code
search results
learning progress
```

AI phải ưu tiên context từ Knowledge Base.

---

# 16. AI Problem Recognition

User có thể nhập đề bài tự do.

Ví dụ:

```text
Nhập n số nguyên, tìm số lớn nhất và nhỏ nhất.
```

Hệ thống phân tích:

```text
Problem Type:
Extreme Value

Pattern:
Maintain Best Candidate

Required Knowledge:
- Variable
- Array
- Loop
- if
- Comparison

Strategy:
1. Initialize
2. Traverse
3. Compare
4. Update
5. Output
```

Sau đó cung cấp:

```text
[Học kiến thức]
[Xem pattern]
[Xem visualization]
[Tự viết code]
[Xem hint]
[Xem solution]
```

AI không được tự tạo taxonomy mới nếu taxonomy tương ứng đã tồn tại trong database.

Nếu không match được taxonomy:

```text
Unclassified
```

và có thể đề xuất cho admin review.

---

# 17. AI Debug

User paste code.

AI phân tích:

```text
Bug
Why
Related Knowledge
Suggested Fix
```

Ví dụ:

```cpp
int max = 0;
```

AI phải có khả năng giải thích vấn đề khi toàn bộ input âm.

Link:

```text
→ Initialization
→ Max/Min Pattern
→ Linear Scan
```

Không chỉ đưa code sửa.

---

# 18. AI Explain Code

Input:

```cpp
for (int i = 0; i < n; i++) {
    sum += a[i];
}
```

Output có thể gồm:

```text
Mục đích
Biến
Điều kiện
Iteration
State changes
Final result
Related concepts
```

Có nút:

```text
[Visualize this code]
```

---

# 19. Visualization Engine

Visualization là core feature của B.

## 19.1. Data visualization

MVP:

```text
Variable
Array
String
Stack
```

## 19.2. Algorithm visualization

MVP:

```text
Linear Search
Binary Search
Bubble Sort
Selection Sort
Insertion Sort
```

## 19.3. Control flow

```text
if
else
for
while
nested loop
break
continue
```

## 19.4. Function

```text
Function call
Parameters
Return
Call stack
Local variables
```

## 19.5. Recursion

```text
Call stack
Base case
Recursive case
Return sequence
```

---

# 20. C++ Execution Trace

Không xây compiler/interpreter C++ riêng.

Kiến trúc:

```text
C++ Code
    ↓
Sandbox
    ↓
Compile
    ↓
Execute
    ↓
Instrumentation / Trace
    ↓
Execution Events
    ↓
Visualization Engine
```

Execution event có thể có dạng:

```json
{
  "step": 12,
  "line": 5,
  "event": "assignment",
  "variables": {
    "i": 3,
    "sum": 6
  }
}
```

Frontend sử dụng trace để:

- Highlight source line.
- Hiển thị variables.
- Hiển thị array state.
- Hiển thị output.
- Step forward/backward.
- Pause/resume/reset.

Controls:

```text
Run
Pause
Step
Reset
Speed
```

---

# 21. C++ Sandbox

Code execution phải được sandbox.

Yêu cầu:

```text
CPU limit
Memory limit
Execution timeout
Process isolation
Filesystem restriction
Network disabled
Output size limit
Source size limit
```

Không cho arbitrary code truy cập host.

Sandbox phải là service riêng.

---

# 22. Code Editor

Editor có:

```text
Syntax highlighting
Line numbers
Autocomplete cơ bản
Run
Reset
Format
Output
Errors
```

Khi compile error:

```text
Compiler Error
    ↓
AI Explain (optional)
    ↓
Related Knowledge
```

---

# 23. Learning Path

Mỗi người mới có một path mặc định:

```text
Programming Basics
 ↓
Variables
 ↓
Input / Output
 ↓
Operators
 ↓
Conditions
 ↓
Loops
 ↓
Functions
 ↓
Arrays
 ↓
Strings
 ↓
Basic Algorithms
 ↓
Recursion
 ↓
Basic STL
```

Mỗi Lesson:

```text
Learn
 ↓
Example
 ↓
Visualization
 ↓
Practice
 ↓
Quiz
 ↓
Complete
```

---

# 24. Progress

Theo dõi:

```text
Lessons completed
Topics viewed
Exercises attempted
Exercises solved
Quiz results
Visualization usage
Weak concepts
Learning history
```

Progress có thể dùng để recommendation.

Ví dụ:

```text
User đang học Search
nhưng Loop mastery thấp

→ Recommend:
Review Loop
```

Recommendation không chỉ dựa trên popularity.

---

# 25. Quiz

Quiz types:

```text
Multiple Choice
True / False
Predict Output
Code Tracing
Find Bug
Choose Pattern
Choose Algorithm
Fill Code
```

Quiz có:

```text
question
options
correct_answer
explanation
related_knowledge
difficulty
```

Sau quiz:

```text
Bạn sai ở:
Loop condition

Ôn lại:
→ for loop
→ loop condition
→ off-by-one error
```

---

# 26. Common Mistakes

Mỗi Topic/Pattern/Exercise nên có lỗi thường gặp.

Ví dụ Loop:

```text
Off-by-one
Infinite loop
Wrong initialization
Wrong update
Incorrect condition
```

Array:

```text
Index out of bounds
Wrong loop boundary
Wrong initialization
```

Max/Min:

```text
Initialize max = 0
Không xử lý array rỗng nếu bài yêu cầu
Duyệt sai phạm vi
```

Common Mistake cũng là Knowledge Node.

---

# 27. Content Architecture

Không nên phụ thuộc hoàn toàn vào database editor.

Source of Truth:

```text
Markdown / YAML / JSON
        ↓
Content Importer
        ↓
PostgreSQL
        ↓
Search Index
```

Ví dụ:

```text
content/
├── course/
├── lessons/
├── concepts/
├── properties/
├── patterns/
├── algorithms/
├── exercises/
├── quizzes/
└── visualizations/
```

Git version-control toàn bộ content.

---

# 28. Content format

Ví dụ:

```yaml
id: array-find-max
type: pattern

title: Tìm giá trị lớn nhất trong mảng

tags:
  - array
  - loop
  - max
  - linear-scan

prerequisites:
  - variable
  - array
  - for-loop
  - comparison

definition: >
  Kỹ thuật duyệt qua các phần tử và duy trì
  giá trị lớn nhất đã tìm thấy.

strategy:
  - Khởi tạo max bằng phần tử đầu tiên.
  - Duyệt các phần tử còn lại.
  - So sánh.
  - Cập nhật max nếu cần.

related:
  - array-find-min
  - array-find-max-position
```

Schema phải được validate trước import.

---

# 29. CMS / Admin

Admin:

```text
Dashboard

Course
├── Chapters
├── Lessons
└── Topics

Knowledge
├── Concepts
├── Properties
├── Rules
├── Patterns
├── Algorithms
└── Mistakes

Exercises
├── Exercise Types
├── Patterns
├── Problems
└── Solutions

Quiz
Visualization
Relations
Tags
Sources
AI Settings
Search Index
```

Content state:

```text
DRAFT
REVIEW
PUBLISHED
ARCHIVED
```

---

# 30. Knowledge Review

AI-generated content:

```text
AI
 ↓
Draft
 ↓
Admin Review
 ↓
Edit
 ↓
Publish
```

Admin phải xem:

```text
Content
Relations
Tags
Source
AI provenance
```

---

# 31. Knowledge Gap Detection

Log những truy vấn không tìm thấy.

Dashboard:

```text
Knowledge Gaps

Query
Search Count
Last Seen
AI fallback used
```

Ví dụ:

```text
Armstrong number
18 searches

Perfect number
11 searches

Frequency array
9 searches
```

Admin có thể:

```text
[Create Knowledge]
```

Từ knowledge gap.

---

# 32. Database Model

Database chính: PostgreSQL.

Các bảng/entity dự kiến:

```text
users
roles
user_progress

courses
course_versions
chapters
lessons
topics

knowledge_items
knowledge_relations
knowledge_tags
tags

patterns
algorithms
techniques

exercise_types
exercises
exercise_knowledge
exercise_patterns
exercise_solutions
exercise_hints

quiz_questions
quiz_options
quiz_attempts

visualizations
visualization_steps

code_runs
execution_traces
execution_events

ai_conversations
ai_messages
ai_requests

search_queries
search_results
knowledge_gaps

content_sources
```

Không nhất thiết tạo tất cả bảng ngay trong migration đầu tiên; triển khai theo milestone.

---

# 33. API Design

Backend: REST API.

Prefix:

```text
/api/v1
```

## Knowledge

```text
GET /knowledge
GET /knowledge/{id}
GET /knowledge/{id}/related
GET /knowledge/{id}/prerequisites
GET /knowledge/{id}/next
GET /knowledge/{id}/graph
```

## Search

```text
GET /search?q=
```

Optional:

```text
type
lesson
tag
difficulty
```

## Exercises

```text
GET /exercises
GET /exercises/{id}
GET /exercises/{id}/related
POST /exercises/{id}/submit
GET /exercises/{id}/solution
```

## Visualization

```text
GET /visualizations/{id}
POST /visualizations/run
```

## Code execution

```text
POST /code/run
POST /code/trace
GET /code/run/{id}
GET /code/run/{id}/trace
```

## AI

```text
POST /ai/explain
POST /ai/hint
POST /ai/analyze-problem
POST /ai/debug
POST /ai/explain-code
POST /ai/search-fallback
```

AI endpoints phải sử dụng shared LLM provider abstraction.

---

# 34. Frontend

Đề xuất:

```text
Next.js
TypeScript
```

Các page chính:

```text
/
 /learn
 /course
 /course/{id}
 /lesson/{id}
 /topic/{id}

 /search
 /exercises
 /exercises/{id}

 /visualize
 /visualize/{id}

 /playground

 /ai

 /progress

 /admin
```

---

# 35. Topic Page UX

Topic page phải có:

```text
Title
Breadcrumb
Definition
Properties
Syntax
Examples
Visualization
Pattern
Problem Types
Solution Method
Common Mistakes
Exercises
Related Knowledge
Prerequisites
Next Knowledge
Knowledge Graph
AI Tutor
```

---

# 36. Search UX

Search bar chính:

```text
Tìm kiếm kiến thức, bài tập, thuật toán...
```

Results grouped:

```text
Tất cả
Bài học
Khái niệm
Tính chất
Pattern
Thuật toán
Bài tập
Phương pháp
```

Nếu không có kết quả:

```text
Không tìm thấy trong Knowledge Base.

[Thử hỏi AI]
```

Không tự động gọi AI.

---

# 37. AI Context Pipeline

AI request phải đi qua:

```text
User Query
 ↓
Search Knowledge Base
 ↓
Retrieve relevant knowledge
 ↓
Build Context
 ↓
LLM
 ↓
Validate / format
 ↓
Response
```

AI prompt phải yêu cầu:

```text
Không bịa knowledge ID.
Không tạo citation giả.
Ưu tiên context được cung cấp.
Nếu thiếu thông tin, nói rõ thiếu.
```

---

# 38. Security

MVP local development nhưng vẫn phải thiết kế an toàn.

Yêu cầu:

```text
Environment variables
No API key in frontend
JWT/session authentication
Admin authorization
Rate limiting cho AI
Sandbox isolation
No host filesystem access
Network disabled trong code runner
Input validation
SQL injection protection
XSS protection
```

LLM API key chỉ tồn tại backend.

---

# 39. Docker

Local development phải chạy bằng Docker Compose.

Services dự kiến:

```text
web
api
worker
postgres
redis
code-runner
```

Optional:

```text
pgadmin
```

Ví dụ:

```text
docker compose up -d
```

Phải có:

```text
.env.example
```

---

# 40. Development Environment

Yêu cầu:

```text
Node.js
Python
Docker
Docker Compose
PostgreSQL
```

README phải có hướng dẫn:

```text
1. Clone
2. Copy .env.example → .env
3. Configure LLM
4. docker compose up
5. Run migrations
6. Seed content
7. Open web
```

---

# 41. Seed Content

Agent phải tạo một bộ Knowledge Base mẫu đủ để demo.

Ít nhất:

```text
10+ Concepts
10+ Properties
10+ Patterns
10+ Algorithms
30+ Exercises
10+ Quiz questions
5+ Visualizations
```

Các content này phải có relation thực tế.

Ví dụ:

```text
Variable
Loop
Array
Find Max
Find Min
Linear Search
Bubble Sort
Function
Recursion
```

---

# 42. Testing

## Backend

```text
Unit tests
API tests
Search tests
Recommendation tests
AI provider tests
```

## Search

Phải test:

```text
Exact query
Vietnamese query
No accent query
Partial query
Typo
Synonym
Natural language
```

Ví dụ:

```text
"tim max mang"
"tìm số lớn nhất trong mảng"
"lấy phần tử lớn nhất"
```

có thể tìm cùng knowledge.

## Recommendation

Test:

```text
Prerequisite
Related
Next
Similar
Exercise-related
Context-aware
```

## Code runner

Test:

```text
Normal code
Compile error
Runtime error
Timeout
Memory limit
Infinite loop
Huge output
Forbidden network
```

---

# 43. Observability

MVP cần logging:

```text
API request
Search query
Search result count
Search latency
AI request
AI latency
Code execution
Execution duration
Errors
```

Không log:

```text
API key
Password
Sensitive credentials
```

---

# 44. Performance

Mục tiêu MVP:

```text
Search response < 500ms
Knowledge page < 1s server-side
Recommendation < 500ms
AI latency phụ thuộc LLM server
```

Search phải có index.

Không load toàn bộ Knowledge Graph.

Chỉ query neighborhood cần thiết.

---

# 45. Accessibility

Frontend cần:

```text
Keyboard navigation
ARIA labels
Readable typography
Code contrast
Focus states
Screen-reader-friendly controls
Reduced motion option
```

Visualization không được là nguồn thông tin duy nhất; phải có textual explanation.

---

# 46. Responsive

Ưu tiên:

```text
Desktop
Tablet
Mobile
```

Code editor và visualization phải usable trên màn hình nhỏ.

---

# 47. Milestone triển khai

## M0 — Project Foundation

```text
- Repository
- Next.js
- FastAPI
- PostgreSQL
- Docker Compose
- Environment config
- Basic CI/test
```

Acceptance:

```text
docker compose up
→ web hoạt động
→ API hoạt động
→ database hoạt động
```

## M1 — Knowledge Base

```text
- Course
- Chapter
- Lesson
- Topic
- Knowledge item
- Content importer
- Admin CRUD
```

Acceptance:

```text
Import YAML/Markdown
→ database
→ topic page
```

## M2 — Knowledge Graph

```text
- Relations
- Prerequisites
- Related
- Next
- Graph API
- Graph UI
```

Acceptance:

```text
Topic
→ related knowledge
→ interactive graph
```

## M3 — Search

```text
- PostgreSQL FTS
- pg_trgm
- pgvector
- Ranking
- Search UI
```

Acceptance:

```text
Natural language query
→ relevant knowledge
```

## M4 — Recommendation Engine

```text
- Relation ranking
- Graph distance
- Context ranking
- Why recommended
```

Acceptance:

```text
Topic/exercise
→ context-aware recommendations
```

## M5 — Exercise Engine

```text
- Exercise taxonomy
- Problem
- Pattern
- Strategy
- Hint
- Solution
- Related exercise
```

Acceptance:

```text
Exercise
→ identify pattern
→ strategy
→ hint
→ solution
```

## M6 — Visualization

```text
- Array
- Variables
- Loop
- Condition
- Function
- Search
- Sorting
- Recursion
```

Acceptance:

```text
Visualization can run step-by-step.
```

## M7 — C++ Execution

```text
- Sandbox
- Compiler
- Execution
- Trace
- Events
- Source highlighting
```

Acceptance:

```text
C++ program
→ run
→ output
→ trace
→ visualize
```

## M8 — AI

```text
- Provider abstraction
- OpenAI-compatible API
- Admin settings
- AI Tutor
- Explain
- Hint
- Debug
- Problem Recognition
- AI fallback
```

Acceptance:

```text
LLM endpoint configurable
without code modification.
```

## M9 — Quiz + Progress

```text
- Quiz
- Attempts
- Progress
- Weak concepts
- Learning path
```

## M10 — Polish

```text
- UX
- Accessibility
- Performance
- Security
- Documentation
- Error handling
- Tests
```

---

# 48. Agent Execution Rules

AI coding agent phải:

1. Đọc toàn bộ `PLAN.md` trước khi code.
2. Không bỏ qua architecture.
3. Không triển khai toàn bộ một lần.
4. Làm từng milestone.
5. Sau mỗi milestone phải chạy test.
6. Không tạo mock thay cho feature thật nếu milestone yêu cầu implementation.
7. Không hard-code API key.
8. Không hard-code LLM provider.
9. Không hard-code syllabus trong UI.
10. Không hard-code recommendation.
11. Không tạo relation chỉ ở frontend.
12. Không để LLM tự quyết định Knowledge Base.
13. Không tự động publish AI-generated content.
14. Không xây C++ compiler riêng.
15. Code runner phải sandbox.
16. Không thêm dependency lớn nếu chưa cần.
17. Ưu tiên open-source.
18. Tất cả service phải chạy local bằng Docker Compose.
19. Viết migration cho schema.
20. Viết seed data cho demo.
21. Viết README và developer documentation.
22. Không xóa/chỉnh sửa dữ liệu người dùng ngoài phạm vi task.
23. Trước khi thay đổi architecture phải cập nhật plan và giải thích trong development notes.

---

# 49. Definition of Done

Một milestone chỉ hoàn thành khi:

```text
[ ] Feature implemented
[ ] API implemented
[ ] UI implemented
[ ] Database migration
[ ] Seed/demo data
[ ] Unit tests
[ ] Integration tests nếu cần
[ ] Error handling
[ ] README/documentation
[ ] Docker support
[ ] No hard-coded secrets
```

---

# 50. MVP Demo Flow

Demo hoàn chỉnh phải cho phép:

```text
User mở homepage
       ↓
Tìm "tìm số lớn nhất trong mảng"
       ↓
Search Engine tìm Knowledge Base
       ↓
Hiển thị:
  - Concept
  - Pattern
  - Method
  - Exercise
       ↓
User mở "Tìm Max"
       ↓
Xem:
  - Definition
  - Required Knowledge
  - Algorithm
  - Visualization
  - Related Knowledge
       ↓
Knowledge Graph
       ↓
Click "Vòng lặp"
       ↓
Học Loop
       ↓
Quay lại Exercise
       ↓
Phân tích Pattern
       ↓
Tự viết C++
       ↓
Run
       ↓
Visualization execution trace
       ↓
Quiz
       ↓
Progress
```

Nếu database không tìm thấy câu hỏi:

```text
User Query
    ↓
Search
    ↓
No sufficient result
    ↓
"Thử hỏi AI?"
    ↓
User confirms
    ↓
Configured self-hosted LLM
    ↓
AI response
    ↓
Related existing Knowledge
    ↓
Optional Save as Draft
```

---

# 51. Nguyên tắc UX quan trọng nhất

Hệ thống không nên tạo cảm giác:

> "Một chatbot biết C++."

Mà phải tạo cảm giác:

> **"Một bản đồ kiến thức C++ có thể tương tác, nơi AI giúp tôi hiểu và học tốt hơn."**

Core loop:

```text
                    ┌───────────────┐
                    │   TRA CỨU     │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │   KIẾN THỨC   │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │ KIẾN THỨC     │
                    │ LIÊN QUAN     │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │ VISUALIZATION │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │    BÀI TẬP    │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │ PHƯƠNG PHÁP   │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │   VIẾT CODE   │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │ EXECUTION     │
                    │ TRACE         │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │      QUIZ     │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │    AI TUTOR   │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │  HỌC TIẾP     │
                    └───────────────┘
```

---

# 52. Future Extensions

Không triển khai trong MVP nhưng architecture phải không chặn:

```text
- Multiple C++ standards
- More programming languages
- Advanced algorithms
- Competitive programming
- Personalized curriculum
- Spaced repetition
- Adaptive exercises
- Classroom / teacher accounts
- Assignment system
- Leaderboard
- Collaborative learning
- Content marketplace
- External knowledge import
- AI-generated exercise drafts
- Automatic visualization generation
```

---

# 53. Architecture Summary

Mục tiêu cuối cùng:

```text
                         ┌───────────────────┐
                         │      FRONTEND     │
                         │ Next.js + React   │
                         └─────────┬─────────┘
                                   │
                          REST / JSON API
                                   │
                         ┌─────────▼─────────┐
                         │      BACKEND      │
                         │      FastAPI      │
                         └─────────┬─────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
          ▼                        ▼                        ▼
 ┌────────────────┐       ┌────────────────┐       ┌────────────────┐
 │ Knowledge      │       │ Exercise       │       │ Visualization  │
 │ Engine         │       │ Engine         │       │ Engine         │
 └───────┬────────┘       └────────────────┘       └───────┬────────┘
         │                                                  │
         ▼                                                  ▼
 ┌────────────────┐                                ┌────────────────┐
 │ Search +       │                                │ C++ Sandbox    │
 │ Recommendation │                                │ + Trace        │
 └───────┬────────┘                                └────────────────┘
         │
         ▼
 ┌────────────────┐
 │ PostgreSQL     │
 │ FTS + pg_trgm  │
 │ + pgvector     │
 └───────┬────────┘
         │
         ▼
 ┌────────────────┐
 │ Content        │
 │ Markdown/YAML  │
 └────────────────┘

                         ┌───────────────────┐
                         │    AI SERVICE     │
                         │ OpenAI-compatible │
                         └─────────▲─────────┘
                                   │
                         Configurable Base URL
                         API Key + Model
```

AI phải là **pluggable service**, Search/Knowledge Base phải hoạt động độc lập khi AI server offline.

---

# 54. Final Product Definition

Sản phẩm hoàn chỉnh phải đáp ứng:

### Tra cứu

```text
✓ Theo bài học
✓ Theo khái niệm
✓ Theo tính chất
✓ Theo pattern
✓ Theo thuật toán
✓ Theo dạng bài
✓ Theo phương pháp giải
✓ Theo kiến thức liên quan
```

### Học

```text
✓ Learning Path
✓ Topic
✓ Example
✓ Visualization
✓ Exercise
✓ Hint
✓ Solution
✓ Quiz
✓ Progress
```

### Interactive

```text
✓ Code editor
✓ C++ execution
✓ Step-by-step execution
✓ Variable visualization
✓ Array visualization
✓ Algorithm visualization
✓ Call stack
```

### AI

```text
✓ Self-hosted LLM
✓ Configurable Base URL
✓ Configurable API Key
✓ Configurable Model
✓ AI Tutor
✓ Explain
✓ Hint
✓ Problem Recognition
✓ Debug
✓ Explain Code
✓ AI fallback search
```

### Knowledge intelligence

```text
✓ Knowledge Graph
✓ Related Knowledge
✓ Prerequisite
✓ Next Knowledge
✓ Similar Knowledge
✓ Context-aware recommendation
✓ Why recommended
✓ Knowledge Gap detection
```

---

# 55. Priority

Nếu phải cắt scope, thứ tự ưu tiên là:

```text
P0
Knowledge Base
Search
Knowledge Relation
Exercise
Recommendation
Basic Visualization

P1
C++ Execution
Execution Trace
Learning Path
Quiz
Progress

P2
AI Tutor
Problem Recognition
AI Debug
AI Search Fallback

P3
Advanced personalization
Advanced visualization
Advanced gamification
```

Không được hy sinh Knowledge Graph, Search và Recommendation để làm chatbot trước.

**Core identity của sản phẩm là Knowledge + Practice + Visualization; AI là lớp thông minh bổ sung lên trên.**

---

# 56. Quyết định sản phẩm và ràng buộc triển khai

Phần này ghi lại các quyết định đã chốt cho phiên bản public. Các milestone và thiết kế chi tiết phải tuân thủ các ràng buộc này.

## 56.1. Mục tiêu phiên bản public

Phiên bản public phải là sản phẩm hoàn chỉnh, có thể vận hành thực tế, bao gồm frontend, backend, database, nội dung, authentication, security, testing, documentation và deployment support.

Bản public phải bao phủ đủ 13 chương trong syllabus. Mỗi chương có chuẩn nội dung tối thiểu đồng nhất:

```text
4 lessons
12 topics / knowledge items
10 exercises
12 quiz questions
3 visualizations
```

Mỗi exercise phải có:

```text
3 tầng hint
1 solution
public test cases
hidden test cases
common mistakes
required knowledge
knowledge relations
```

Tổng tối thiểu dự kiến:

```text
52 lessons
156 knowledge items
130 exercises
156 quiz questions
39 visualizations
```

Các con số trên là ngưỡng tối thiểu; nội dung phức tạp có thể có nhiều hơn nếu cần để bảo đảm chất lượng sư phạm.

## 56.2. Ngôn ngữ và fallback nội dung

Frontend, admin, content, search taxonomy, quiz, exercise và AI phải hỗ trợ tiếng Việt và tiếng Anh ngay từ đầu.

Mỗi nội dung được quản lý theo locale độc lập. Cho phép publish khi chỉ có một bản dịch. Nếu thiếu locale được yêu cầu, hệ thống dùng bản dịch còn lại và hiển thị rõ trạng thái fallback cho người dùng.

## 56.3. Tài khoản và quyền

Hệ thống có hai role:

```text
LEARNER
ADMIN
```

Learner bắt buộc đăng ký/đăng nhập bằng username và password. Không yêu cầu email trong phiên bản public đầu tiên.

Yêu cầu bảo mật tài khoản:

```text
Password tối thiểu 8 ký tự
Argon2id
Session cookie HttpOnly, Secure, SameSite
Rate limit đăng nhập thất bại
Logout toàn bộ session
Admin có thể khóa tài khoản và đặt lại password
Không log password hoặc credential
```

Progress, code run, submission, quiz attempt và AI conversation phải được kiểm tra quyền sở hữu, tránh IDOR giữa các learner.

## 56.4. Content CMS và backup

Database/CMS là nguồn chính của nội dung production.

```text
Admin CMS
    ↓
PostgreSQL
    ↓
Publish trực tiếp
    ↓
Export snapshot sang Git
```

Admin được sửa trực tiếp nội dung đang public. Mỗi thay đổi phải ghi audit log gồm người sửa, thời điểm, entity, trường thay đổi và giá trị trước/sau phù hợp với chính sách dữ liệu. Hệ thống nên tạo snapshot trước khi sửa để hỗ trợ khôi phục.

Backup do Admin thực hiện thủ công khi cần. Phải có chức năng:

```text
Export database/content/configuration
Import/restore với preview và xác nhận
Kiểm tra compatibility/version trước restore
Hiển thị thời điểm export gần nhất
Cảnh báo dữ liệu phát sinh sau lần backup cuối có thể bị mất
```

Import snapshot không được ghi đè âm thầm dữ liệu hiện tại.

## 56.5. C++ execution và submission

Execution profile public cố định ở:

```text
C++17
```

Có hai workflow riêng:

```text
Run
    → chạy với input do learner cung cấp
    → trả output/compiler error/runtime error

Submit
    → chạy public và hidden test cases
    → trả kết quả chấm mà không làm lộ hidden tests
```

Execution trace điều khiển process đang chạy theo thời gian thực trong phạm vi các cấu trúc thuộc 13 chương. Job trace phải có process supervisor, authenticated runner channel, timeout cứng, cleanup khi client mất kết nối và giới hạn CPU, memory, process/thread, file descriptor, filesystem, network và output.

Trace state tối thiểu:

```text
QUEUED
RUNNING
PAUSED
COMPLETED
FAILED
TIMED_OUT
CANCELLED
```

Nếu instrumentation hoặc cấu trúc code không được hỗ trợ, hệ thống vẫn compile/run/chấm bình thường và thông báo rõ rằng execution trace không khả dụng. Không tạo trace giả.

Runner không được truy cập host filesystem, Docker socket, credential hoặc network ngoài policy. Cơ chế isolation cụ thể phải được xác định trong thiết kế security trước khi triển khai public.

## 56.6. AI và LLM server

AI là bắt buộc trong bản public và phải có các mode:

```text
AI Tutor
Hint
Explain
Explain Code
Debug
Problem Recognition
Generate Quiz
Search Fallback
```

LLM chạy trên server riêng, được ứng dụng gọi qua mạng nội bộ bằng OpenAI-compatible API. Core Knowledge Base, Search, Exercise, Quiz và Code Runner phải hoạt động khi LLM offline.

AI có thể nhận toàn bộ context cần thiết cho request hiện tại:

```text
user query
relevant knowledge
exercise/problem context
user code
compiler/runtime error
relevant progress
current conversation history
```

Không gửi password, API key hoặc dữ liệu tài khoản không cần thiết. Response phải được đánh dấu AI-generated, validate theo schema khi có cấu trúc, và citation/knowledge ID phải được server kiểm tra trước khi hiển thị.

## 56.7. Search mặc định

Search public hỗ trợ:

```text
Exact
Keyword / PostgreSQL FTS
Vietnamese có dấu và không dấu
Fuzzy typo / pg_trgm
Tag và filter
Relation-aware
Semantic / vector
Unified ranking
```

Search phải có lexical fallback khi vector index hoặc embedding service chưa sẵn sàng hay gặp lỗi. Ranking không được phụ thuộc duy nhất vào LLM.

Pipeline embedding phải gắn với content version và embedding model version. Search benchmark phải bao gồm query có dấu, không dấu, tự nhiên, synonym và typo; acceptance phải dùng metric top-k và latency thay vì chỉ mô tả “relevant”.

## 56.8. Graph Recommendation Engine

Graph algorithm được dùng cho Knowledge Graph và Recommendation, không thay thế toàn bộ content search. Luồng chuẩn là:

```text
Content Search
    ↓
Initial candidates
    ↓
Optional graph traversal/ranking
    ↓
Context-aware recommendations
```

Hệ thống phải có setting ở cấp Admin để bật/tắt graph engine. Khi tắt, lỗi, timeout hoặc vượt giới hạn tài nguyên, hệ thống tự động dùng search và relation trực tiếp mặc định; không làm request thất bại chỉ vì graph engine.

Cấu hình tối thiểu:

```text
graph_engine_enabled
recommendation_strategy
max_graph_depth
max_nodes_visited
max_recommendations
algorithm_timeout_ms
```

Chiến lược algorithm:

```text
BFS
    Tìm prerequisite/related trong neighborhood theo số bước.

Dijkstra
    Tìm đường đi và xếp hạng khi relation có trọng số.

DFS
    Validation reachability và phát hiện cycle; không dùng làm ranking chính.

A*
    Tìm learning path tới một target cụ thể; tắt mặc định cho recommendation thông thường.
```

Strategy mặc định production là BFS cho neighborhood. Dijkstra chỉ được dùng khi trọng số relation đã được xác định và kiểm thử. A* phải được bật riêng cho goal-oriented learning path, không tự động dùng cho mọi request.

Graph engine phải ghi lại strategy, latency, node count, depth và lý do fallback. Relation trực tiếp do Admin quản lý luôn là nguồn ưu tiên hơn các cạnh suy luận từ graph traversal.

## 56.9. Learning completion

Một lesson chỉ được đánh dấu hoàn thành khi learner thỏa tất cả điều kiện:

```text
Đã mở và đọc lesson
Đã xem ít nhất một example hoặc visualization
Quiz đạt tối thiểu 70%
Đã submit accepted ít nhất một exercise bắt buộc
```

Exercise dùng hint nhiều tầng:

```text
Hint 1 → Hint 2 → Hint 3 → Solution
```

Solution luôn có thể mở. Việc sử dụng từng hint và solution phải được ghi nhận để phục vụ progress và recommendation.

## 56.10. Tiêu chí hoàn tất public

Dự án chỉ được coi là hoàn tất khi đạt toàn bộ Definition of Done tại mục 49 và MVP Demo Flow tại mục 50, bao gồm:

```text
Frontend, backend và database hoạt động
Đủ 13 chương và dữ liệu demo thực tế
Authentication và authorization
Search đầy đủ và có lexical fallback
Graph recommendation có setting và fallback
Exercise hidden-test judging
Visualization và realtime trace trong phạm vi đã cam kết
AI đầy đủ qua LLM server nội bộ
Admin CMS và export/restore
Security, accessibility, responsive và performance
Unit, integration, API, security và end-to-end tests
README và tài liệu triển khai public
```

Mỗi milestone phải có acceptance theo user journey, không chỉ checklist tồn tại của API/UI.

## 56.11. Technology stack

Stack chính của hệ thống:

```text
Frontend:
  Next.js + TypeScript
  Tailwind CSS + shadcn/ui
  Monaco Editor
  React Flow + D3.js

Backend:
  FastAPI + Python
  SQLAlchemy 2.x
  Pydantic 2.x
  Alembic
  REST API /api/v1

Database and search:
  PostgreSQL
  PostgreSQL Full-Text Search
  pg_trgm
  pgvector

Async processing:
  Redis
  Celery workers

Infrastructure:
  Docker Compose
  Reverse proxy (Nginx hoặc Caddy)
```

Code runner phải là service riêng, không chạy trực tiếp trong tiến trình API. LLM service chạy trên máy chủ riêng và giao tiếp với backend qua mạng nội bộ.

Không thêm graph database riêng trong phiên bản public đầu tiên. PostgreSQL là nơi lưu trữ canonical cho Knowledge Graph; các cạnh được lưu trong `knowledge_relations` cùng relation type, weight và metadata cần thiết.

## 56.12. Graph storage và algorithm service

PostgreSQL chịu trách nhiệm lưu node, edge, ràng buộc dữ liệu và cung cấp neighborhood/candidate graph. Graph algorithms chạy ở backend trong Graph/Recommendation Service, không phụ thuộc vào việc PostgreSQL có triển khai sẵn các thuật toán đó hay không.

```text
PostgreSQL
  → knowledge_items
  → knowledge_relations
  → lấy node/edge cần thiết

Graph / Recommendation Service
  → BFS
  → DFS
  → Dijkstra
  → A*

Recommendation API
  → ranking
  → progress context
  → why recommended
```

Schema cạnh tối thiểu:

```text
knowledge_relations
  id
  source_id
  target_id
  relation_type
  weight
  is_active
  metadata
```

Quy tắc sử dụng algorithm:

```text
BFS:
  Tìm prerequisite/related theo neighborhood và số bước.

DFS:
  Kiểm tra reachability và phát hiện cycle trong graph validation;
  không dùng làm ranking chính.

Dijkstra:
  Tìm đường đi hoặc xếp hạng khi relation có weight đã được kiểm thử.

A*:
  Tìm learning path tới target cụ thể;
  không tự động dùng cho recommendation thông thường.
```

Graph Service phải giới hạn độ sâu, số node đã duyệt, số recommendation, thời gian chạy và xử lý cycle/duplicate edge. Các truy vấn graph đơn giản có thể dùng PostgreSQL `WITH RECURSIVE`, nhưng không dùng recursive SQL làm implementation chính cho Dijkstra hoặc A*.

Graph engine luôn là lớp tùy chọn phía trên content search. Khi setting bị tắt hoặc Graph Service lỗi/timeout, hệ thống fallback về PostgreSQL FTS, `pg_trgm`, pgvector và relation trực tiếp theo ranking mặc định; search và recommendation không được thất bại chỉ vì graph algorithm.
