from dataclasses import dataclass


@dataclass
class Queries:
    categories_query: str = """query categories ($courseId: String!){
  course (sisId: $courseId) {
    _id
    groupSetsConnection {
      nodes {
        name
        _id
      }
    }
  }
}"""
    sections_query: str = """query sections($courseId: String!) {
  course(sisId: $courseId) {
    sectionsConnection {
      nodes {
        name
        sisId
      }
    }
  }
}"""
    groups_query: str = """query groups($courseId: String!) {
  course(sisId: $courseId) {
    groupsConnection {
      nodes {
        _id
        membersCount
        membersConnection {
          nodes {
            _id
            user {
              _id
            }
          }
        }
        name
        sisId
      }
    }
  }
}"""

    all_users_query: str = """query curso($courseId: ID!) {
  course(id: $courseId) {
    enrollmentsConnection{
      nodes {
        sisRole
        section {
          name
        }
        user {
          _id
          loginId
          enrollments(courseId: $courseId, currentOnly: true) {
            type
            state
          }
        }
      }
    }
  }
}
"""
    groups_mutation: str = """mutation CreateGroups($groupName1: String!, $groupName2: String!, $groupName3: String!, $groupName4: String!, $groupName5: String!, $groupName6: String!, $groupName7: String!, $groupName8: String!, $groupName9: String!, $groupName10: String!, $cateogryId: ID!) {
  group1: createGroupInSet(input: {name: $groupName1, groupSetId: $cateogryId}) {
    group {
      _id
      name
      sisId
    }
    errors {
      attribute
      message
    }
  }
  group2: createGroupInSet(input: {name: $groupName2, groupSetId: $cateogryId}) {
    group {
      _id
      name
      sisId
    }
    errors {
      attribute
      message
    }
  }
  group3: createGroupInSet(input: {name: $groupName3, groupSetId: $cateogryId}) {
    group {
      _id
      name
      sisId
    }
    errors {
      attribute
      message
    }
  }
  group4: createGroupInSet(input: {name: $groupName4, groupSetId: $cateogryId}) {
    group {
      _id
      name
      sisId
    }
    errors {
      attribute
      message
    }
  }
  group5: createGroupInSet(input: {name: $groupName5, groupSetId: $cateogryId}) {
    group {
      _id
      name
      sisId
    }
    errors {
      attribute
      message
    }
  }
  group6: createGroupInSet(input: {name: $groupName6, groupSetId: $cateogryId}) {
    group {
      _id
      name
      sisId
    }
    errors {
      attribute
      message
    }
  }
  group7: createGroupInSet(input: {name: $groupName7, groupSetId: $cateogryId}) {
    group {
      _id
      name
      sisId
    }
    errors {
      attribute
      message
    }
  }
  group8: createGroupInSet(input: {name: $groupName8, groupSetId: $cateogryId}) {
    group {
      _id
      name
      sisId
    }
    errors {
      attribute
      message
    }
  }
  group9: createGroupInSet(input: {name: $groupName9, groupSetId: $cateogryId}) {
    group {
      _id
      name
      sisId
    }
    errors {
      attribute
      message
    }
  }
  group10: createGroupInSet(input: {name: $groupName10, groupSetId: $cateogryId}) {
    group {
      _id
      name
      sisId
    }
    errors {
      attribute
      message
    }
  }
}
"""
