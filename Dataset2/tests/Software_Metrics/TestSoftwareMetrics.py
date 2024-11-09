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
            file_content = "//Questo è un commento single-line in Java}"
            expected_output = ""  # Rimuove i commenti single-line

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
                /* Questo è un commento 
                multilinea */
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
                x--; 
            } else {  if (y > 0) { y++; }}"""
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
            file_content = "public interface NomeInterfaccia {}"
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            declarative_lines = sm.count_declarative_lines()

            assert declarative_lines == expected_output

        def test_case_7(self):
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

        def test_case_8(self):
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

        def test_case_9(self):
            file_content = """
            @Option
            public class MyClass {}
            """
            expected_output = 2

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            declarative_lines = sm.count_declarative_lines()

            assert declarative_lines == expected_output

        def test_case_10(self):
            file_content = """
            public static final int MAX_VALUE = 100;
            """
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            declarative_lines = sm.count_declarative_lines()

            assert declarative_lines == expected_output

        def test_case_11(self):
            file_content = """
                import java.util.List;
            """
            expected_output = 1

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            declarative_lines = sm.count_declarative_lines()

            assert declarative_lines == expected_output

        def test_case_12(self):
            file_content = """
            import java.util.List;
            @Deprecated
            public class MyClass {
                private int x;
                public void myMethod() {}
            }
            public interface NomeInterfaccia {
                void metodoAstratto();
            }
            """
            expected_output = 7

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
        def test_case_1(self):
            file_content = '''
            public class Main {
                int §c;
            }'''

            with pytest.raises(LexerError):
                base_dir = os.path.dirname(os.getcwd())
                sm = SoftwareMetrics(base_dir, "path_file", file_content)
                sm.compute_essential_complexity_metrics()

        def test_case_2(self):
            file_content = '''
            public class Main {
                int +;
            }'''

            base_dir = os.path.dirname(os.getcwd())
            with pytest.raises(JavaSyntaxError):
                sm = SoftwareMetrics(base_dir, "path_file", file_content)
                sm.compute_essential_complexity_metrics()

        def test_case_3(self):
            file_content = '''
            public class Main {
            }
            '''

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            mec, sec = sm.compute_essential_complexity_metrics()

            assert mec == 0
            assert sec == 0

        def test_case_4(self):
            file_content = '''
            public class Main {
                int var1, var2;
            
                public Main(int var1, int var2){
                    this.var1 = var1;
                    this.var2 = var2;
                }
            
                public void setVar1(int var1){
                    this.var1 = var1;
                }
            
                public int method1(){
                    int a = 1;
                    int b = 0;
            
                    
                    try {
                        return a / b;  
                    }
                    catch (Exception e) {
                        while (b == 0) {
                            for (int i = 0; i < 2; i++) { 
                                do {
                                    synchronized (this) {
                                        if(a<4)
                                           break;
                                    }
                                } while (b < 3);
                            }
                        }
        
                        switch (a) {
                            case -1:
                                return a;
                            case -2:
                                b++;
                                break;
                            case -3:
                                return b;
                        }
        
                    }
                    
                    catch (NullPointerException e) {
                        System.out.println("Exception");
                    }
                     
                    finally {
                        System.out.println("Operation closed");  
                    }
            
                    return b;  
                }
            }
            '''

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            mec, sec = sm.compute_essential_complexity_metrics()
            assert mec == 10
            assert sec == 12

        def test_case_5(self):
            file_content = '''
            public class Main {
                int var1, var2;

                public void setVar1(int var1){
                    this.var1 = var1;
                }

                public int method1(){
                    int a = 1;
                    int b = 0;


                    {
                        a = b + 1;
                        b = a + 2*b;
                        System.out.println(a);
                    }

                    return b;  // Fallback return in case no other return is reached
                }
            }
            '''

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            mec, sec = sm.compute_essential_complexity_metrics()
            assert mec == 1
            assert sec == 2

        def test_case_6(self):
            file_content = '''
            public class Main {
                int var1, var2;
                
                public Main(int var1, int var2){
                
                  if(var1>var2)
                    var1=var1+var2;
                  else
                    var2=var1+var2;
                
                  this.var1=var1;
                  this.var2=var2;
                
                }
            
            }
            '''

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            mec, sec = sm.compute_essential_complexity_metrics()
            assert mec == 1
            assert sec == 1

        def test_case_7(self):
            file_content = '''
            public class Main {
                int var1, var2;

                public int method_1(){
                    int a, b;

                    if(a>b){
                        a=a-b;
                        setVar(a);
                        return a;
                    }
                    else{
                        b=b+1;
                        return b;
                    }


                }

                public void setVar1(int var){
                    this.var1 = var;
                }

            }
            '''

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            mec, sec = sm.compute_essential_complexity_metrics()
            assert mec == 1
            assert sec == 2

        def test_case_8(self):
            file_content = '''
            public class Main {
                int var1, var2;

                public int method_1(){
                    int a, b;
                    
                    if(a>b){
                        a=a-b;
                        setVar(a);
                        return a;
                    }
                    
                    if(a==b){
                        return b;
                    }
                    else{
                       setVar(b);
                       return b-a;
                    }
                    
                    
                }
                
                public void setVar1(int var){
                    this.var1 = var;
                }

            }
            '''

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            mec, sec = sm.compute_essential_complexity_metrics()
            assert mec == 3
            assert sec == 4



        def test_case_9(self):
            file_content = '''
            public class Main {
                int var1, var2;

                public int method_1(int a, int b){

                    while(a<b){
                       a=a*2; 
                    }
                    
                    while(a>b){
                       a=a-2;
                       setvar2(b);
                       break;
                    }
                    
                    while(1){
                       a=a+2;
                       setvar2(b);
                       break;
                    }
                    
                    setVar1(a);
                    
                    return a;

                }

                public void setVar1(int var){
                    this.var1 = var;
                }
                
                public void setVar2(int var){
                    this.var2 = var;
                }

            }
            '''

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            mec, sec = sm.compute_essential_complexity_metrics()
            assert mec == 1
            assert sec == 3

        def test_case_10(self):
            file_content = '''
            public class Main {
                int var1, var2;

                public float method_1(){
                    float a=0;
                    float b=1;

                    for(int i=0; i<3; i++){
                        a=a*i+2*i;
                        b=b+1;
                    }

                    setVar1(a);
                    
                    for(int j=1; j<4; j++){
                        setVar1(b);
                        break;
                    }
                    
                    for(int z=10; z>9; z--){
                        a = a*z;
                        break;
                    }

                    return a;

                }

                public void setVar1(int var){
                    this.var1 = var;
                }

            }
            '''

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            mec, sec = sm.compute_essential_complexity_metrics()
            assert mec == 1
            assert sec == 2

        def test_case_11(self):
            file_content = '''
            public class Main {
                int var1, var2;
                
                public int method_1(int a, int b){
                
                  do{
                    a=a+1;
                    break;
                  }while(a>2);
                
                  do{
                    b=b*2;
                    break;
                  }while(a>2);
                
                
                    do{
                      b=b+1;
                      return b;
                    }while(a>2);
                
                }
                
            }
            '''

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            mec, sec = sm.compute_essential_complexity_metrics()
            assert mec == 1
            assert sec == 1

        def test_case_12(self):
            file_content = '''
            public class Main {
                int var1, var2;

                public int method_1(int a, int b){

                  switch(a){
                    case 1: return a;
                  }
                  
                  switch(b){
                    case 2: return b;
                  }

                }
            }
            '''

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            mec, sec = sm.compute_essential_complexity_metrics()
            assert mec == 3
            assert sec == 3

        def test_case_13(self):
            file_content = '''
            public class Main {
                int var1, var2;
                
                public int method_1(int a, int b){
                
                  switch(a){
                    case 1: a++;
                    case 2: System.out.println(a); break;
                    case 3: b++;
                    case 4: return b;
                  }
                
                }
            }
            '''

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            mec, sec = sm.compute_essential_complexity_metrics()
            assert mec == 5
            assert sec == 5

        def test_case_14(self):
            file_content = '''
            public class Main {
                int var1, var2;

                public int method_1(int a, int b){

                  switch(a){
                    case 1: a++; break;
                    case 2: System.out.println(a); break;
                    case 3: b++; break;
                    case 4: a++; return a; break;
                  }
                  
                  return b;

                }
            }
            '''

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            mec, sec = sm.compute_essential_complexity_metrics()
            assert mec == 5
            assert sec == 5

        def test_case_15(self):
            file_content = '''
            public class Main {
                int var1, var2;

                public int method_1(int a, int b){

                  switch(a){
                    case 1: a++;
                    case 2: System.out.println(a);
                    case 3: b++;
                    case 4: System.out.println(b); break;
                  }
                  
                  return b;

                }
            }
            '''

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            mec, sec = sm.compute_essential_complexity_metrics()
            assert mec == 5
            assert sec == 5

        def test_case_16(self):
            file_content = '''
            public class Main {
                int var1, var2;

                public int method_1(int a, int b){

                  switch(a){
                    case 1: a++; break;
                    case 2: System.out.println(a); break;
                    case 3: b++; break;
                    case 4: System.out.println(b); break;
                  }

                  return b;

                }
            }
            '''

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            mec, sec = sm.compute_essential_complexity_metrics()
            assert mec == 1
            assert sec == 1

        def test_case_17(self):
            file_content = '''
            public class Main {
                int var1, var2;
                
                public int method_1(int a, int b){
                
                  try{
                    File myObj = new File("filename.txt");
                    Scanner myReader = new Scanner(myObj);
                    String data = myReader.nextLine(); 
                  }
                  finally {
                    while(a<1)
                      if(b)
                        break;
                  }
                
                
                }
            }
            '''

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            mec, sec = sm.compute_essential_complexity_metrics()
            assert mec == 3
            assert sec == 3

        def test_case_18(self):
            file_content = '''
            public class Main {
                int var1, var2;

                public int method_1(int a, int b){

                  try{
                    File myObj = new File("filename.txt");
                    Scanner myReader = new Scanner(myObj);
                    String data = myReader.nextLine(); 
                    return a;
                  }
                  catch(ArithmeticException  e){
                     System.out.println("Exception detected");
                  }
                  catch(NullPointerException e){
                     System.out.println("Exception detected");
                  }
                

                }
            }
            '''

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            mec, sec = sm.compute_essential_complexity_metrics()
            assert mec == 3
            assert sec == 3

        def test_case_19(self):
            file_content = '''
            public class Main {
                int var1, var2;

                public int method_1(int a, int b){

                  try{
                    File myObj = new File("filename.txt");
                    Scanner myReader = new Scanner(myObj);
                    String data = myReader.nextLine(); 
                    return a;
                  }
                  catch(ArithmeticException  e){
                     System.out.println("Exception detected");
                     return 0;
                  }

                }
            }
            '''

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            mec, sec = sm.compute_essential_complexity_metrics()
            assert mec == 1
            assert sec == 1

        def test_case_20(self):
            file_content = '''
            public class Main {
                int var1, var2;

                public int method_1(int a, int b){

                  try{
                    File myObj = new File("filename.txt");
                    Scanner myReader = new Scanner(myObj);
                    String data = myReader.nextLine(); 
                    return a;
                  }
                  catch(ArithmeticException  e){
                     System.out.println("Exception detected");
                     return 0;
                  }
                  catch(NullPointerException e){
                     System.out.println("Exception detected");
                     return -1;
                  }


                }
            }
            '''

            base_dir = os.path.dirname(os.getcwd())
            sm = SoftwareMetrics(base_dir, "path_file", file_content)
            mec, sec = sm.compute_essential_complexity_metrics()
            assert mec == 3
            assert sec == 3


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

        @patch('Dataset2.Software_Metrics.SoftwareMetrics.logging.getLogger')
        def test_case_3(self, mock_getLogger):
            mock_logger = MagicMock()
            mock_getLogger.return_value = mock_logger

            base_dir = os.path.dirname(os.getcwd())
            file_path = "existing_file.java"
            file_content = """public class Test {
                    void method() {
                        int x = 10
                        @#invalid_token
                    }
                }"""

            sm = SoftwareMetrics(base_dir, file_path, file_content)
            sm.analyze()

            mock_logger.error.assert_called_once_with(
                "Errore nell'analisi del file existing_file.java: Il file presenta un carattere o una sequenza di caratteri non valida.")

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
            file_content = "public class Test { public void method() { int x = 'string'; } }"

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
                    if (x==0)
                        x++;
                }
            }
            """

            sm = SoftwareMetrics(base_dir, file_path, file_content)
            result = sm.analyze()

            expected_max = 3
            expected_sum = 6

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
