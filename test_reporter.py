# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

file = ET.parse('test_result.xml')

root = file.getroot()

tests = []

totalGoldenTestDuration = 0.0

totalScreenTestDuration = 0.0

class Test:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

testReport = open('test_report.txt', 'w+')

print('')
print('╔═════════════════════╗')
print('║ Extract Test Result ║')
print('╚═════════════════════╝')
print('')

testReport.write('╔═════════════════════╗\n')
testReport.write('║ Extract Test Result ║\n')
testReport.write('╚═════════════════════╝\n\n')

for testSuite in root:
    fullPackage = testSuite.get('name')
    totalTestError = testSuite.get('errors')
    totalTestSkipped = testSuite.get('skipped')
    totalTest = testSuite.get('tests')

    isGoldenTest = False

    if ('core.bazaar' in fullPackage):
        isGoldenTest = True

    lastPackage = fullPackage.rsplit('.', 1)[1].capitalize()

    screenTestDurationPerPackage = 0.0

    goldenTestDurationPerPackage = 0.0

    testCases = []

    for testCase in testSuite:
        name = testCase.attrib.get('name')
        time = testCase.attrib.get('time')

        if (name != None and time != None):
            additionalTime = float(time)

            if (isGoldenTest):
                totalGoldenTestDuration += additionalTime
                goldenTestDurationPerPackage += additionalTime
            else:
                totalScreenTestDuration += additionalTime
                screenTestDurationPerPackage += additionalTime

            test = Test(name, time)
            tests.append(test)
            testCases.append(test)

    testReport.write('╔═══ {0}/\n║\n'.format(lastPackage))
    print('╔═══ {0}/'.format(lastPackage))
    print('║')

    for testIndex in range(0, len(testCases)):
        test = testCases[testIndex]
        
        testReport.write('║  ╔ {0}\n'.format(test.name))
        testReport.write('║  ╚ Duration: {0} ms\n'.format(test.duration))

        print('║  ╔ {0}'.format(test.name))
        print('║  ╚ Duration: {0} ms'.format(test.duration))

    totalTestSucces = int(totalTest) - int(totalTestError)
    testReport.write('║\n╚═══ Total Duration: {0} ms (Success: {1}, Errors: {2}, Skipped: {3})\n'.format(screenTestDurationPerPackage, totalTestSucces, totalTestError, totalTestSkipped))
    print('║')
    print('╚═══ Total Duration: {0} ms (Success: {1}, Errors: {2}, Skipped: {3})\n'.format(screenTestDurationPerPackage, totalTestSucces, totalTestError, totalTestSkipped))

tests.sort(key=lambda test: test.duration, reverse=True)

print('')
print('╔════════════════════════════╗')
print('║ Total Screen Test Duration ║')
print('╚════════════════════════════╝')
print('╚ {0} ms\n'.format(totalScreenTestDuration))

testReport.write('\n╔════════════════════════════╗\n║ Total Screen Test Duration ║\n╚════════════════════════════╝\n')
testReport.write('╚ {0} ms\n\n'.format(totalScreenTestDuration))

print('')
print('╔════════════════════════════╗')
print('║ Total Golden Test duration ║')
print('╚════════════════════════════╝')
print('╚ {0} ms\n'.format(totalGoldenTestDuration))

testReport.write('╔════════════════════════════╗\n║ Total Golden Test duration ║\n╚════════════════════════════╝\n')
testReport.write('╚ {0} ms\n\n'.format(totalGoldenTestDuration))

print('')
print('╔════════════════════╗')
print('║ The 5 Longest Test ║')
print('╚════════════════════╝')
print('')

testReport.write('╔════════════════════╗\n║ The 5 Longest Test ║\n╚════════════════════╝\n')

for index in range(0, 5):
    test = tests[index]
    print('╔ {0}. {1}'.format(index + 1, test.name))
    print('╚ Duration: {0} ms'.format(test.duration))
    testReport.write('╔ {0}. {1}\n╚ Duration: {2} ms\n'.format(index + 1, test.name, test.duration))

testReport.close()
