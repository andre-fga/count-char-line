from collections import Counter
import sublime
import sublime_plugin

class GenerateLineCharReportCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        window = view.window()
        if not window:
            return

        lines = view.lines(sublime.Region(0, view.size()))
        total_lines = len(lines)

        length_counts = Counter()
        detailed_lines = []

        # Processa as linhas e calcula os tamanhos
        for i, line_region in enumerate(lines, start=1):
            line_text = view.substr(line_region)
            char_count = len(line_text)
            length_counts[char_count] += 1
            detailed_lines.append(f"L{i:04d} [{char_count} chars]: {line_text}")

        # Monta o cabeçalho com o agrupamento de contagens
        report = []
        report.append("=" * 60)
        report.append(" CHARACTER COUNT PER LINE REPORT ")
        report.append("=" * 60)
        report.append(f"Lines: {total_lines}")
        report.append("\n--- FREQUENCY SUMMARY (GROUPING) ---")
        report.append("Size (chars)  |  Number of Lines")
        report.append("-" * 40)

        # Ordena do menor tamanho para o maior
        for length in sorted(length_counts.keys()):
            count = length_counts[length]
            report.append(f"{length:>15} chars  ->  {count} lines")

        report.append("\n" + "=" * 60)
        report.append(" Line-by-line breakdown ")
        report.append("=" * 60 + "\n")
        report.extend(detailed_lines)

        full_output = "\n".join(report)

        # Abre uma nova aba e insere o texto gerado
        new_view = window.new_file()
        new_view.set_name("Relatorio_Caracteres.txt")
        new_view.set_scratch(True)  # Não solicita salvar ao fechar
        new_view.run_command("insert_report_content", {"text": full_output})


class InsertReportContentCommand(sublime_plugin.TextCommand):
    def run(self, edit, text):
        self.view.insert(edit, 0, text)