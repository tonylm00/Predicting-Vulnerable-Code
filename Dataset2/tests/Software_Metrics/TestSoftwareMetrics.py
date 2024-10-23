import os
from unittest.mock import patch, MagicMock
import pytest
from javalang.parser import JavaSyntaxError
from javalang.tokenizer import LexerError
from Dataset2.Software_Metrics.SoftwareMetrics import SoftwareMetrics

class TestSoftwareMetrics:
    def test_case_1(self):
        base_dir = "invalid_directory"
        file_content = ""

        with pytest.raises(FileNotFoundError):
            SoftwareMetrics(base_dir, "path_file", file_content)

    class TestRemoveComments:
        def test_case_1(self):
            base_dir = os.path.dirname(os.getcwd())
            file_content = ""
            expected_output = ""

            sm = SoftwareMetrics(base_dir, "path_file", file_content)

            assert sm.file_content == expected_output

        def test_case_2(self):
            file_content = """/*
                Questo è un commento multilinea in Java
                che copre più righe
            */"""
            expected_output = ""
            base_dir = os.path.dirname(os.getcwd())

            sm = SoftwareMetrics(base_dir, "path_file", file_content)

            assert sm.file_content.strip() == expected_output.strip()

        def test_case_3(self):
            base_dir = os.path.dirname(os.getcwd())
            file_content = "public class Test {\n    // Questo è un commento single-line in Java\n    public void test() { System.out.println(\"Hello World\"); }\n}"
            expected_output = "public class Test {\n     \n    public void test() { System.out.println(\"Hello World\"); }\n}"  # Rimuove i commenti single-line

            sm = SoftwareMetrics(base_dir, "path_file", file_content)

            assert sm.file_content.strip() == expected_output.strip()

        def test_case_4(self):
            base_dir = os.path.dirname(os.getcwd())
            file_content = "System.out.println(\"Questo non è un commento // ma parte della stringa\");"
            expected_output = "System.out.println(\"Questo non è un commento // ma parte della stringa\");"  # Commenti nelle stringhe rimangono

            sm = SoftwareMetrics(base_dir, "path_file", file_content)

            assert sm.file_content == expected_output

        def test_case_5(self):
            base_dir = os.path.dirname(os.getcwd())
            file_content = "public class Test {\n    public void test() { System.out.println(\"Hello World\"); }\n}"
            expected_output = "public class Test {\n    public void test() { System.out.println(\"Hello World\"); }\n}"  # Codice senza commenti rimane invariato

            sm = SoftwareMetrics(base_dir, "path_file", file_content)

            assert sm.file_content == expected_output

        def test_case_6(self):
            base_dir = os.path.dirname(os.getcwd())
            file_content = """public class Test {
            // Questo è un commento single-line
            public void test() { 
                /* Questo è un commento multilinea */
                System.out.println("Hello World"); 
            }
            /** Questo è un commento docstring */
            }"""
            expected_output = """public class Test {
             
            public void test() { 
                 
                System.out.println("Hello World"); 
            }
             
            }"""

            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            assert sm.file_content.strip() == expected_output.strip()

        def test_case_7(self):
            base_dir = "invalid_directory"
            file_content = ""

            with pytest.raises(FileNotFoundError):
                SoftwareMetrics(base_dir, "path_file", file_content)

    class TestCalculateMaxNesting:
        def test_case_1(self):
            base_dir = os.path.dirname(os.getcwd())
            file_content = ""
            expected_output = 0

            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            max_nesting = sm.calculate_max_nesting()

            assert max_nesting == expected_output

        def test_case_2(self):
            base_dir = os.path.dirname(os.getcwd())
            file_content = "if () { "
            expected_output = 1

            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            max_nesting = sm.calculate_max_nesting()

            assert max_nesting == expected_output

        def test_case_3(self):
            base_dir = os.path.dirname(os.getcwd())
            file_content = "int x = 'a'; @#InvalidToken"
            expected_output = 0

            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            max_nesting = sm.calculate_max_nesting()

            assert max_nesting == expected_output

        def test_case_4(self):
            base_dir = os.path.dirname(os.getcwd())
            file_content = "int x = 0;"
            expected_output = 0

            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            max_nesting = sm.calculate_max_nesting()

            assert max_nesting == expected_output

        def test_case_5(self):
            base_dir = os.path.dirname(os.getcwd())
            file_content = "if (x > 0) { x++; }"
            expected_output = 1

            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            max_nesting = sm.calculate_max_nesting()

            assert max_nesting == expected_output

        def test_case_6(self):
            base_dir = os.path.dirname(os.getcwd())
            file_content = """if (x > 0) { x++; }
        else { x--; }"""
            expected_output = 1

            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            max_nesting = sm.calculate_max_nesting()

            assert max_nesting == expected_output

        def test_case_7(self):
            base_dir = os.path.dirname(os.getcwd())
            file_content = """if (x > 0) {
            if (y > 0) { y++; }
        } else { x--; }"""
            expected_output = 2

            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            max_nesting = sm.calculate_max_nesting()

            assert max_nesting == expected_output

        def test_case_8(self):
            file_content = """if (x > 0) x++;
                else x--;"""
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            max_nesting = sm.calculate_max_nesting()

            assert max_nesting == expected_output

        def test_case_9(self):
            file_content = """if (x > 0) 
            { y++; } 
            else  if (y > 0) x--; """
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            max_nesting = sm.calculate_max_nesting()

            assert max_nesting == expected_output

        def test_case_10(self):
            file_content = """for (int i = 0; i < 10; i++) {
            System.out.println(i);
            }"""
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            max_nesting = sm.calculate_max_nesting()

            assert max_nesting == expected_output

        def test_case_11(self):
            file_content = """while (x < 10) {
                x++; }"""
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            max_nesting = sm.calculate_max_nesting()

            assert max_nesting == expected_output

        def test_case_12(self):
            file_content = """do {
            x++; } while (x < 10);"""
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            max_nesting = sm.calculate_max_nesting()

            assert max_nesting == expected_output

        def test_case_13(self):
            file_content = """switch (x) {
            case 1:
                x++; break;
            case 2:
                x--; break;
            }"""
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            max_nesting = sm.calculate_max_nesting()

            assert max_nesting == expected_output

        def test_case_14(self):
            file_content = """try {
                x++;
            } catch (Exception e) {
                x--;
            }"""
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            max_nesting = sm.calculate_max_nesting()

            assert max_nesting == expected_output

        def test_case_15(self):
            file_content = """
            if (x > 0) { x++; }
            for (int i = 0; i < 10; i++) { x--; }
            while (x < 5) { x++; }
            do { x--; } while (x > 0);
            switch (x) { case 1: x++; break; }
            try { x++; } catch (Exception e) { x--; }
            """
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            max_nesting = sm.calculate_max_nesting()

            assert max_nesting == expected_output

        def test_case_16(self):
            file_content = """
            if (x > 0) {
                for (int i = 0; i < 10; i++) {
                    if (x%2 == 0) {
                        while (x < 5) {
                            x++;
                        }
                    }
                }
            } else {
                switch (x) {
                    case 1:
                        try {
                            x++;
                        } catch (Exception e) {
                            x--;
                        }
                        break;
                }
            }"""
            expected_output = 4

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            max_nesting = sm.calculate_max_nesting()

            assert max_nesting == expected_output

        def test_case_17(self):
            file_content = """
            if (x > 0) { 
                for (int i = 0; i < 10; i++) {
                    x++;
                }
                if (x > 1) {
                    while (x < 5) { x--; }
                }
            } else {
                switch (x) {
                    case 1:
                        try {
                            x++;
                        } catch (Exception e) {
                            x--;
                        }
                        break;
                }
            }"""
            expected_output = 3

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            max_nesting = sm.calculate_max_nesting()

            assert max_nesting == expected_output

        def test_case_18(self):
            file_content = """
            if (x > 0) { /* commento */
                x++;
            } else {
                x--;
            }"""
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            max_nesting = sm.calculate_max_nesting()

            assert max_nesting == expected_output

    class TestCountDeclarativeLines:
        def test_case_1(self):
            file_content = ""
            expected_output = 0

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            declarative_lines = sm.count_declarative_lines()

            assert declarative_lines == expected_output

        def test_case_2(self):
            file_content = "public class { int x = 10 }"
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            declarative_lines = sm.count_declarative_lines()

            assert declarative_lines == expected_output

        def test_case_3(self):
            file_content = "public class MyClass { int x = 'text' @#InvalidToken }"
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            declarative_lines = sm.count_declarative_lines()

            assert declarative_lines == expected_output

        def test_case_4(self):
            file_content = "System.out.println('Hello World');"
            expected_output = 0

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            declarative_lines = sm.count_declarative_lines()

            assert declarative_lines == expected_output

        def test_case_5(self):
            file_content = "public class MyClass {}"
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            declarative_lines = sm.count_declarative_lines()

            assert declarative_lines == expected_output

        def test_case_6(self):
            file_content = """
            public class MyClass {
                public void myMethod() {}
            }
            """
            expected_output = 2

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            declarative_lines = sm.count_declarative_lines()

            assert declarative_lines == expected_output

        def test_case_7(self):
            file_content = """
            public class MyClass {
                private int x = 10;
            }
            """
            expected_output = 2

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            declarative_lines = sm.count_declarative_lines()

            assert declarative_lines == expected_output

        def test_case_8(self):
            file_content = """
            @Option
            public class MyClass {}
            """
            expected_output = 2

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            declarative_lines = sm.count_declarative_lines()

            assert declarative_lines == expected_output

        def test_case_9(self):
            file_content = """
            public static final int MAX_VALUE = 100;
            """
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            declarative_lines = sm.count_declarative_lines()

            assert declarative_lines == expected_output

        def test_case_9(self):
            file_content = """
                import java.util.List;
            """
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            declarative_lines = sm.count_declarative_lines()

            assert declarative_lines == expected_output

        def test_case_10(self):
            file_content = """
            import java.util.List;
            @Deprecated
            public class MyClass {
                private int x;
                public void myMethod() {}
            }
            """
            expected_output = 5

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            declarative_lines = sm.count_declarative_lines()

            assert declarative_lines == expected_output

    class TestCountLinesOfCode:
        def test_case_1(self):
            file_content = ""
            expected_output = 0

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            loc = sm.count_lines_of_code()

            assert loc == expected_output

        def test_case_2(self):
            file_content = "int x = ;"
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            loc = sm.count_lines_of_code()

            assert loc == expected_output

        def test_case_3(self):
            file_content = "int x = 'string' @#InvalidToken"
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            loc = sm.count_lines_of_code()

            assert loc == expected_output

        def test_case_4(self):
            file_content = "int x = 10;"
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            loc = sm.count_lines_of_code()

            assert loc == expected_output

        def test_case_5(self):
            file_content = "// Questo è un commento"
            expected_output = 0

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            loc = sm.count_lines_of_code()

            assert loc == expected_output

        def test_case_6(self):
            file_content = """
            int x = 10;
            int y = 20;
            """
            expected_output = 2

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            loc = sm.count_lines_of_code()

            assert loc == expected_output

        def test_case_7(self):
            file_content = """
            // Questo è un commento
            int x = 10;
            """
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            loc = sm.count_lines_of_code()

            assert loc == expected_output

        def test_case_8(self):
            file_content = """
            // Commento 1
            // Commento 2
            """
            expected_output = 0

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            loc = sm.count_lines_of_code()

            assert loc == expected_output

        def test_case_9(self):
            file_content = """
            /* Questo è un commento 
            multilinea */
            int x = 10;
            """
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            loc = sm.count_lines_of_code()

            assert loc == expected_output

        def test_case_10(self):
            file_content = """
            /* Commento 
            multilinea  */
            """
            expected_output = 0

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            loc = sm.count_lines_of_code()

            assert loc == expected_output

        def test_case_11(self):
            file_content = """

            int x = 10;

            int y = 20;

            """
            expected_output = 2

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            loc = sm.count_lines_of_code()

            assert loc == expected_output

    class TestCountMethodsDeclaration:
        def test_case_1(self):
            file_content = ""
            expected_output = 0

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            method_count = sm.count_method_declarations()

            assert method_count == expected_output

        def test_case_2(self):
            file_content = "void myMethod( {"
            expected_output = 0

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            method_count = sm.count_method_declarations()

            assert method_count == expected_output

        def test_case_3(self):
            file_content = "void myMethod() { return @#InvalidToken 'string'; }"
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            method_count = sm.count_method_declarations()

            assert method_count == expected_output

        def test_case_4(self):
            file_content = "int x = 10;"
            expected_output = 0

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            method_count = sm.count_method_declarations()

            assert method_count == expected_output

        def test_case_5(self):
            file_content = """
            public void method1() {}
            private int method2() { return 0; }
            """
            expected_output = 2

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            method_count = sm.count_method_declarations()

            assert method_count == expected_output

        def test_case_6(self):
            file_content = """
            public MyClass() {}
            public MyClass(int x) { this.x = x; }
            """
            expected_output = 2

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            method_count = sm.count_method_declarations()

            assert method_count == expected_output

        def test_case_7(self):
            file_content = """
            Runnable r = () -> System.out.println("Hello");
            Callable<Integer> c = () -> 42;
            """
            expected_output = 2

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            method_count = sm.count_method_declarations()

            assert method_count == expected_output

        def test_case_8(self):
            file_content = """
            Runnable r = new Runnable() {
                public void run() {
                    System.out.println("Running");
                }
            };
            """
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            method_count = sm.count_method_declarations()

            assert method_count == expected_output

        def test_case_9(self):
            file_content = """
            public MyClass() {}
            public void method1() {}
            Runnable r = () -> System.out.println("Hello");
            """
            expected_output = 3

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            method_count = sm.count_method_declarations()

            assert method_count == expected_output

    class TestCountClassDeclaration:
        def test_case_1(self):
            file_content = ""
            expected_output = 0

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            class_count = sm.count_class_declarations()

            assert class_count == expected_output

        def test_case_2(self):
            file_content = "class MyClass {"
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            class_count = sm.count_class_declarations()

            assert class_count == expected_output

        def test_case_3(self):
            file_content = "int x = 'string'; @#InvalidToken"
            expected_output = 0

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            class_count = sm.count_class_declarations()

            assert class_count == expected_output

        def test_case_4(self):
            file_content = "import java.util.List;"
            expected_output = 0

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            class_count = sm.count_class_declarations()

            assert class_count == expected_output

        def test_case_5(self):
            file_content = """
            public class MyClass {
                private int x;
            }
            """
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            class_count = sm.count_class_declarations()

            assert class_count == expected_output

        def test_case_6(self):
            file_content = """
            public interface MyInterface {
                void method1();
            }
            """
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            class_count = sm.count_class_declarations()

            assert class_count == expected_output

        def test_case_7(self):
            file_content = """
            public class MyClass {
                Runnable r = new Runnable() {
                    public void run() {
                        System.out.println("Running");
                    }
                };
            }
            """
            expected_output = 2

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            class_count = sm.count_class_declarations()

            assert class_count == expected_output

        def test_case_8(self):
            file_content = """
            public class OuterClass {
                private class InnerClass {
                    private int y;
                }
            }
            """
            expected_output = 2

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            class_count = sm.count_class_declarations()

            assert class_count == expected_output

        def test_case_9(self):
            file_content = """
            // Dichiarazione di classe
            public class OuterClass {
                // Classe nidificata
                private class InnerClass {
                    private int y;
                }

                // Classe anonima
                Runnable r = new Runnable() {
                    public void run() {
                        System.out.println("Running");
                    }
                };

                // Dichiarazione di metodo
                public void outerMethod() {
                    // Metodo che utilizza una classe anonima
                    Callable<Integer> c = new Callable<Integer>() {
                        public Integer call() {
                            return 42;
                        }
                    };
                }
            }

            // Dichiarazione di interfaccia
            public interface MyInterface {
                void myMethod();
            }
            """

            expected_output = 5

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            class_count = sm.count_class_declarations()

            assert class_count == expected_output

    class TestComputeEssentialComplexity:
        def test_compute_essential_complexity(self):
            pass

    class TestAnalyze:
        def test_case_1(self):
            base_dir = os.path.dirname(os.getcwd())
            file_path = "existing_file.java"
            file_content = ""

            sm = SoftwareMetrics(base_dir, file_path, file_content)
            result = sm.analyze()

            expected_max = 0
            expected_sum = 0

            assert result['MaxCyclomaticStrict'] == expected_max
            assert result['SumCyclomaticStrict'] == expected_sum

        @patch('Dataset2.Software_Metrics.SoftwareMetrics.logging.getLogger')
        def test_case_2(self, mock_getLogger):
            mock_logger = MagicMock()
            mock_getLogger.return_value = mock_logger

            base_dir = os.path.dirname(os.getcwd())
            file_path = "existing_file.java"
            file_content = "public class Test {"

            sm = SoftwareMetrics(base_dir, file_path, file_content)
            sm.analyze()

            mock_logger.error.assert_called_once_with("Errore nell'analisi del file existing_file.java: Il file non presenta una sintassi java valida.")

        def test_case_3(self):
            base_dir = os.path.dirname(os.getcwd())
            file_path = "existing_file.java"
            file_content = "public class Test { public void method() { int x = 'string'; } }"

            sm = SoftwareMetrics(base_dir, file_path, file_content)
            result = sm.analyze()

            expected_max = 1
            expected_sum = 1

            assert result['MaxCyclomaticStrict'] == expected_max
            assert result['SumCyclomaticStrict'] == expected_sum

        def test_case_4(self):
            base_dir = os.path.dirname(os.getcwd())
            file_path = "existing_file.java"
            file_content = "public class Test {}"

            sm = SoftwareMetrics(base_dir, file_path, file_content)
            result = sm.analyze()

            expected_max = 0
            expected_sum = 0

            assert result['MaxCyclomaticStrict'] == expected_max
            assert result['SumCyclomaticStrict'] == expected_sum

        def test_case_5(self):
            base_dir = os.path.dirname(os.getcwd())
            file_path = "existing_file.java"
            file_content = "public class Test { public void method() {} }"

            sm = SoftwareMetrics(base_dir, file_path, file_content)
            result = sm.analyze()

            expected_max = 1
            expected_sum = 1

            assert result['MaxCyclomaticStrict'] == expected_max
            assert result['SumCyclomaticStrict'] == expected_sum

        def test_case_6(self):
            base_dir = os.path.dirname(os.getcwd())
            file_path = "existing_file.java"
            file_content = "public class Test { public void method() { if (true) {} } }"

            sm = SoftwareMetrics(base_dir, file_path, file_content)
            result = sm.analyze()

            expected_max = 2
            expected_sum = 2

            assert result['MaxCyclomaticStrict'] == expected_max
            assert result['SumCyclomaticStrict'] == expected_sum

        def test_case_7(self):
            base_dir = os.path.dirname(os.getcwd())
            file_path = "existing_file.java"
            file_content = """
            public class Test {
                public void method() {
                    if (true) {
                        while (true) {}
                    }
                }
            }
            """

            sm = SoftwareMetrics(base_dir, file_path, file_content)
            result = sm.analyze()

            expected_max = 3
            expected_sum = 3

            assert result['MaxCyclomaticStrict'] == expected_max
            assert result['SumCyclomaticStrict'] == expected_sum

        def test_case_8(self):
            base_dir = os.path.dirname(os.getcwd())
            file_path = "existing_file.java"
            file_content = """
            public class Test {
                public void method1() {}
                public void method2() {}
            }
            """

            sm = SoftwareMetrics(base_dir, file_path, file_content)
            result = sm.analyze()

            expected_max = 1
            expected_sum = 2

            assert result['MaxCyclomaticStrict'] == expected_max
            assert result['SumCyclomaticStrict'] == expected_sum

        def test_case_9(self):
            base_dir = os.path.dirname(os.getcwd())
            file_path = "existing_file.java"
            file_content = """
            public class Test {
                public void method1() { if (true) {} }
                public void method2() { if (true) {} }
            }
            """

            sm = SoftwareMetrics(base_dir, file_path, file_content)
            result = sm.analyze()

            expected_max = 2
            expected_sum = 4

            assert result['MaxCyclomaticStrict'] == expected_max
            assert result['SumCyclomaticStrict'] == expected_sum

        def test_case_10(self):
            base_dir = os.path.dirname(os.getcwd())
            file_path = "existing_file.java"
            file_content = """
            public class Test {
                public void method1() {
                    if (true) {
                        while (true) {}
                    }
                }
                public void method2() {
                    for (int i = 0; i < 10; i++) {}
                }
            }
            """

            sm = SoftwareMetrics(base_dir, file_path, file_content)
            result = sm.analyze()

            expected_max = 3
            expected_sum = 5

            assert result['MaxCyclomaticStrict'] == expected_max
            assert result['SumCyclomaticStrict'] == expected_sum

        def test_case_11(self):
            base_dir = os.path.dirname(os.getcwd())
            file_path = ""

            file_content = """
                        public class Test {
                            public void method() {
                                if (true) {
                                    while (true) {}
                                }
                            }
                        }
                        """

            sm = SoftwareMetrics(base_dir, file_path, file_content)
            result = sm.analyze()

            expected_max = 3
            expected_sum = 3

            assert result['MaxCyclomaticStrict'] == expected_max
            assert result['SumCyclomaticStrict'] == expected_sum

        def test_case_12(self):
            base_dir = os.path.dirname(os.getcwd())
            file_path = "existing_file.txt"

            file_content = """
                        public class Test {
                            public void method() {
                                if (true) {
                                    while (true) {}
                                }
                            }
                        }
                        """

            sm = SoftwareMetrics(base_dir, file_path, file_content)
            result = sm.analyze()

            expected_max = 3
            expected_sum = 3

            assert result['MaxCyclomaticStrict'] == expected_max
            assert result['SumCyclomaticStrict'] == expected_sum
