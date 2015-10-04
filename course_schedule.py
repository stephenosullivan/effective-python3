__author__ = 'stephenosullivan'

class Solution(object):
    def canFinish(self, numCourses, prerequisites):
        """
        :type numCourses: int
        :type prerequisites: List[List[int]]
        :rtype: bool
        """
        prereqDict = dict()
        futureSubject = dict()

        for subject, prereq in prerequisites:
            if subject in prereqDict:
                prereqDict[subject].append(prereq)
            else:
                prereqDict[subject] = [prereq]

            if prereq in futureSubject:
                futureSubject[prereq].append(subject)
            else:
                futureSubject[prereq] = [subject]


        # Initial classes have no prereqs
        queue = [num for num in range(numCourses) if num not in prereqDict]
        completed = set()
        to_complete = set(range(numCourses))
        while queue:
            subject = queue.pop()
            if subject not in completed:

                # Newly completed subject
                completed.add(subject)
                to_complete.remove(subject)

                if subject in futureSubject:
                    for sub in futureSubject[subject]:
                        prereqDict[sub].remove(subject)

                    # No more prerequisites for future classes
                    for sub in futureSubject[subject]:
                        if not prereqDict[sub]:
                            queue.append(sub)

        if to_complete:
            return False
        return True

