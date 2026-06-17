// ============================================================
// Module 3 – Hands On 5: MongoDB – Feedback Collection
// Cognizant DN5.0 | Harish Seetharaman Rama
// Run in: mongosh  OR  MongoDB Compass Shell
// ============================================================

// STEP 1: Select database
use college_nosql

// ============================================================
// TASK 1: Create Collection & Insert 10+ Documents
// ============================================================

db.feedback.insertMany([
  {
    student_id: 1,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 5,
    comments: "Excellent teaching. Concepts explained very clearly.",
    tags: ["challenging", "well-structured", "good-examples"],
    submitted_at: new Date("2022-11-30T10:15:00Z"),
    attachments: [{ filename: "notes.pdf", size_kb: 240 }]
  },
  {
    student_id: 2,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 4,
    comments: "Very good course. Would recommend.",
    tags: ["challenging", "informative"],
    submitted_at: new Date("2022-11-28T09:00:00Z"),
    attachments: [{ filename: "summary.pdf", size_kb: 180 }]
  },
  {
    student_id: 5,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 3,
    comments: "Average experience. Could be better.",
    tags: ["average", "needs-improvement"],
    submitted_at: new Date("2022-11-29T14:30:00Z"),
    attachments: []
  },
  {
    student_id: 1,
    course_code: "CS102",
    semester: "2022-ODD",
    rating: 4,
    comments: "Good course on databases. Hands-on was helpful.",
    tags: ["well-structured", "practical"],
    submitted_at: new Date("2022-12-01T11:00:00Z"),
    attachments: [{ filename: "db_notes.pdf", size_kb: 320 }]
  },
  {
    student_id: 2,
    course_code: "CS102",
    semester: "2022-ODD",
    rating: 2,
    comments: "Too fast paced. Needed more examples.",
    tags: ["fast-paced", "needs-improvement"],
    submitted_at: new Date("2022-12-02T08:45:00Z")
    // intentionally no attachments field — schema-less design allows this
  },
  {
    student_id: 3,
    course_code: "EC101",
    semester: "2021-ODD",
    rating: 5,
    comments: "Best professor in the department.",
    tags: ["engaging", "well-structured", "good-examples"],
    submitted_at: new Date("2021-11-25T10:00:00Z"),
    attachments: []
  },
  {
    student_id: 6,
    course_code: "EC101",
    semester: "2021-EVEN",
    rating: 1,
    comments: "Did not enjoy this course at all.",
    tags: ["boring", "needs-improvement"],
    submitted_at: new Date("2021-12-10T16:00:00Z"),
    attachments: []
  },
  {
    student_id: 4,
    course_code: "ME101",
    semester: "2023-ODD",
    rating: 4,
    comments: "Interesting subject with good lab sessions.",
    tags: ["practical", "informative"],
    submitted_at: new Date("2023-11-20T13:00:00Z"),
    attachments: [{ filename: "lab_report.pdf", size_kb: 410 }]
  },
  {
    student_id: 7,
    course_code: "ME101",
    semester: "2021-EVEN",
    rating: 3,
    comments: "Average course. Theory was heavy.",
    tags: ["average", "theory-heavy"],
    submitted_at: new Date("2021-12-05T10:00:00Z"),
    attachments: []
  },
  {
    student_id: 8,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 5,
    comments: "Outstanding! Loved the problem solving sessions.",
    tags: ["challenging", "well-structured", "engaging"],
    submitted_at: new Date("2022-11-27T09:30:00Z"),
    attachments: [{ filename: "practice_problems.pdf", size_kb: 150 }]
  }
])

// Verify count
db.feedback.countDocuments()   // should return 10

// ============================================================
// TASK 2: CRUD Operations
// ============================================================

// READ 1: Find all feedback with rating 5
db.feedback.find({ rating: 5 })

// READ 2: CS101 feedback where tags contain 'challenging'
db.feedback.find({
  course_code: "CS101",
  tags: "challenging"
})

// READ 3: Projection — student_id, course_code, rating only (no _id)
db.feedback.find(
  {},
  { student_id: 1, course_code: 1, rating: 1, _id: 0 }
)

// UPDATE 1: Add needs_review: true to all docs with rating < 3
db.feedback.updateMany(
  { rating: { $lt: 3 } },
  { $set: { needs_review: true } }
)

// UPDATE 2: Push tag 'reviewed' to all docs where needs_review is true
db.feedback.updateMany(
  { needs_review: true },
  { $push: { tags: "reviewed" } }
)

// DELETE: Remove all feedback from semester '2021-EVEN'
db.feedback.deleteMany({ semester: "2021-EVEN" })

// Verify remaining count
db.feedback.countDocuments()

// ============================================================
// TASK 3: Aggregation Pipeline
// ============================================================

// Pipeline 1: Filter 2022-ODD → Group by course → Sort by avg rating
db.feedback.aggregate([
  { $match: { semester: "2022-ODD" } },
  {
    $group: {
      _id: "$course_code",
      avg_rating: { $avg: "$rating" },
      total_feedback: { $sum: 1 }
    }
  },
  { $sort: { avg_rating: -1 } }
])

// Pipeline 2: Same as above + $project to rename and round avg_rating
db.feedback.aggregate([
  { $match: { semester: "2022-ODD" } },
  {
    $group: {
      _id: "$course_code",
      avg_rating: { $avg: "$rating" },
      total_feedback: { $sum: 1 }
    }
  },
  {
    $project: {
      course_code: "$_id",
      average_rating: { $round: ["$avg_rating", 1] },
      total_feedback: 1,
      _id: 0
    }
  },
  { $sort: { average_rating: -1 } }
])

// Pipeline 3: Tag frequency leaderboard using $unwind
db.feedback.aggregate([
  { $unwind: "$tags" },
  {
    $group: {
      _id: "$tags",
      count: { $sum: 1 }
    }
  },
  { $sort: { count: -1 } }
])

// Task 3 – Index on course_code + verify with explain
db.feedback.createIndex({ course_code: 1 })

db.feedback.find({ course_code: "CS101" }).explain("executionStats")
// Look for: "stage": "IXSCAN" instead of "COLLSCAN" ✅
