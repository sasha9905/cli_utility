from typing import List


class RPMVersionComparator:

    @staticmethod
    def _compare_segments(seg1: str, seg2: str) -> int:
        """
        Сравнивает два сегмента по правилам RPM.
        """
        # В RPM пустая строка считается "новее" любой непустой строки
        if seg1 == "" and seg2 == "":
            return 0
        if seg1 == "":
            return 1
        if seg2 == "":
            return -1

        # Проверяем, начинается ли строка с тильды
        seg1_has_tilde = seg1.startswith('~')
        seg2_has_tilde = seg2.startswith('~')

        # Если одна строка начинается с тильды, а другая нет
        if seg1_has_tilde and not seg2_has_tilde:
            return -1  # строка с тильдой "старше" (меньше)
        if not seg1_has_tilde and seg2_has_tilde:
            return 1  # строка без тильды "новее" (больше)

        # Если обе начинаются с тильды, убираем одну тильду и сравниваем дальше
        if seg1_has_tilde and seg2_has_tilde:
            # Убираем по одной тильде
            seg1 = seg1[1:]
            seg2 = seg2[1:]
            # Рекурсивно сравниваем (могут быть множественные тильды)
            return RPMVersionComparator._compare_segments(seg1, seg2)

        # Теперь строки не пустые и без тильд (или с одинаковым количеством тильд)
        # Проверяем, являются ли сегменты числами
        seg1_is_num = seg1.isdigit()
        seg2_is_num = seg2.isdigit()

        if seg1_is_num and not seg2_is_num:
            return 1
        if not seg1_is_num and seg2_is_num:
            return -1

        if seg1_is_num and seg2_is_num:
            # Сравниваем как целые числа
            num1, num2 = int(seg1), int(seg2)
            if num1 < num2:
                return -1
            elif num1 > num2:
                return 1
            else:
                return 0
        else:
            # Оба не числа - сравниваем как строки
            if seg1 < seg2:
                return -1
            elif seg1 > seg2:
                return 1
            else:
                return 0

    @staticmethod
    def _split_into_segments(part: str) -> List[str]:
        """
        Разбиение на сегменты.
        """
        if not part:
            return []

        segments = []
        current = ""

        i = 0
        while i < len(part):
            char = part[i]

            if char.isdigit():
                # Собираем все цифры подряд
                start = i
                while i < len(part) and part[i].isdigit():
                    i += 1
                segments.append(part[start:i])
                continue
            elif char.isalpha():
                # Собираем все буквы подряд
                start = i
                while i < len(part) and part[i].isalpha():
                    i += 1
                segments.append(part[start:i])
                continue
            else:
                # Не цифра и не буква - одиночный символ
                segments.append(char)
                i += 1

        return segments

    @staticmethod
    def _compare_version_parts(part1: str, part2: str) -> int:
        """Сравнивает version или release части."""
        # пустая строка (отсутствие release) < любая непустая строка
        if part1 == "" and part2 == "":
            return 0
        if part1 == "" and part2 != "":
            return -1  # пустая < непустая
        if part1 != "" and part2 == "":
            return 1  # непустая > пустая

        # Теперь обе строки непустые, проверяем тильды
        if part1.startswith('~') and not part2.startswith('~'):
            return -1
        if not part1.startswith('~') and part2.startswith('~'):
            return 1

        # Разбиваем на сегменты
        segments1 = RPMVersionComparator._split_into_segments(part1)
        segments2 = RPMVersionComparator._split_into_segments(part2)

        # Сравниваем сегменты один за другим
        for i in range(max(len(segments1), len(segments2))):
            seg1 = segments1[i] if i < len(segments1) else ""
            seg2 = segments2[i] if i < len(segments2) else ""

            result = RPMVersionComparator._compare_segments(seg1, seg2)
            if result != 0:
                return result

        return 0

    @staticmethod
    def compare_versions(epoch1: int, ver1: str, rel1: str,
                         epoch2: int, ver2: str, rel2: str) -> int:
        """
        Сравнивает две полные RPM версии.
        Returns:
            -1 если version1 < version2
             0 если version1 == version2
             1 если version1 > version2
        """
        if epoch1 < epoch2:
            return -1
        elif epoch1 > epoch2:
            return 1

        ver_cmp = RPMVersionComparator._compare_version_parts(ver1, ver2)
        if ver_cmp != 0:
            return ver_cmp

        return RPMVersionComparator._compare_version_parts(rel1, rel2)

